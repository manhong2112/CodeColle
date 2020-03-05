import java.io.InputStream
import java.io.FileOutputStream
import java.nio.file.Paths
import java.nio.file.Files
import java.io.ByteArrayOutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.regex.Matcher
import java.util.regex.Pattern
import scala.util.control.Breaks._
import scala.concurrent._
import scala.concurrent.duration.DurationInt
import scala.util.{Success, Failure}

import org.json.JSONObject;

object PixivDownload {
  implicit val ec: scala.concurrent.ExecutionContext =
    scala.concurrent.ExecutionContext.global

  def main(args: Array[String]): Unit = {
    for (arg <- args) {
      println(arg)
    }
    val params = parseArgs(args)
    val pid = params("pid")
    val dest = params.get("dest").getOrElse(".")
    Files.createDirectories(Paths.get(dest))

    Await.result(
      getMeta(pid)
        .flatMap {
          case (date, illustType, num) =>
            parseExt(pid, date).map { ext =>
              (date, num, ext)
            }
        }
        .flatMap {
          case (date, num, ext) =>
            Future.sequence(
              (0 until num)
                .map({
                  i =>
                    val url =
                      s"https://i.pximg.net/img-original/img/${date}/${pid}_p${i}.${ext}"
                    println(s"I> Downloading from '${url}'")
                    getImg(date, pid, i, ext).andThen {
                      case Success(img) =>
                        val name = s"${dest}/${pid}_p${i}.${ext}"
                        println(s"I> Saving ${pid} to ${name}")
                        val f = new FileOutputStream(name)
                        f.write(img)
                        f.close()
                      case Failure(ex) =>
                        println(s"E> Failed downloading ${pid}")
                        println(ex.getMessage())
                    }
                })
            )
        }
        .andThen({
          case Success(value) =>
            println("I> Success")
          case Failure(exception) =>
            println("E> Failed")
        }),
      10.seconds
    )
  }

  // => Date, IllustType, PageCount
  def getMeta(pid: String): Future[(String, Int, Int)] = {
    val url = s"https://www.pixiv.net/ajax/user/1/illusts?ids[]=${pid}"
    GET(url).map { s =>
      val obj = new JSONObject(new String(s, "UTF8"));
      val picMeta = obj.getJSONObject("body").getJSONObject(pid)
      val p = Pattern.compile(
        s"(\\d{4}/\\d{2}/\\d{2}/\\d{2}/\\d{2}/\\d{2})/${pid}_p0"
      )
      val m = p.matcher(picMeta.getString("url"))
      m.find()
      (m.group(1), picMeta.getInt("illustType"), picMeta.getInt("pageCount"))
    }
  }

  def parseExt(pid: String, date: String): Future[String] = {
    def parseOneExt(ext: String): Future[String] = {
      Future {
        val url =
          s"https://i.pximg.net/img-original/img/${date}/${pid}_p0.${ext}"
        val conn =
          (new URL(url)).openConnection().asInstanceOf[HttpURLConnection]
        conn.setRequestMethod("HEAD")
        List("referer" -> url).map { h =>
          conn.setRequestProperty(h._1, h._2)
        }
        conn.connect()
        if (conn.getResponseCode() == 200) Some(ext) else None
      }.flatMap {
        case Some(value) => Future.successful(value)
        case None        => Future.failed(new Exception("E> Failed to get extension"))
      }
    }
    parseOneExt("jpg")
      .recoverWith {
        case _ =>
          parseOneExt("png")
      }
  }

  def parseData(pid: String): Future[(String, Int)] = {
    val img_page = s"https://www.pixiv.net/artworks/${pid}"
    val header = List("referer" -> img_page)
    GET(img_page, header)
      .map {
        case v =>
          val res = new String(v, "UTF8")
          val p = Pattern.compile(
            s"(\\d{4}/\\d{2}/\\d{2}/\\d{2}/\\d{2}/\\d{2})/${pid}_p0_master1200"
          )
          val p2 = Pattern.compile(
            s""" ":\\{"illustId":"${pid}",[^}]*?"pageCount":(\\d+)," """.trim()
          )
          val m = p.matcher(res)
          val m2 = p2.matcher(res)
          m.find()
          m2.find()
          (m.group(1), m2.group(1).toInt)
      }
  }

  def getImg(
      date: String,
      pid: String,
      page: Int,
      ext: String
  ): Future[Array[Byte]] = {
    // https://i.pximg.net/img-original/img/2019/11/23/03/09/00/77944010_p0.jpg
    val url =
      s"https://i.pximg.net/img-original/img/${date}/${pid}_p${page}.${ext}"
    GET(url, List("referer" -> url))
  }

  def parseArgs(args: Array[String]): Map[String, String] = {
    args.map { x =>
      if (x.contains("=")) {
        val y = x.split("=")
        y(0) -> y(1)
      } else {
        x -> "true"
      }
    }.toMap
  }

  def GET(
      url: String,
      header: List[(String, String)] = List()
  ): Future[Array[Byte]] = {
    val conn = (new URL(url)).openConnection().asInstanceOf[HttpURLConnection]
    header.map { h =>
      conn.setRequestProperty(h._1, h._2)
    }

    Future {
      conn.connect()
      val status = conn.getResponseCode()
      if (!(status >= 300)) {
        val is = conn.getInputStream()

        val buffer = new ByteArrayOutputStream()
        val data = new Array[Byte](4096)
        var nRead = -1

        while ({
          nRead = is.read(data, 0, data.length)
          if (nRead != -1) {
            buffer.write(data, 0, nRead)
          }
          nRead != -1
        }) ()

        is.close()
        buffer.flush()
        buffer.toByteArray()
      } else {
        throw new Exception(s"Failed to get response: status(${status})")
      }
    }
  }
}

// =' ω '=
