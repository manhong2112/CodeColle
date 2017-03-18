import java.io.InputStream;
import java.io.FileOutputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.HashMap;

class HttpResponseException extends Exception {
    private int code;
    public HttpResponseException(int code) {
        this.code = code;
    }
    public int getResponseCode() {
        return this.code;
    }
}

public class PixivDownload {
    // http://i1.pixiv.net/img-original/img/<date&time>/<pid>_p<page>.<\d{3}>
    public static void main(String[] args) {
        final String downloadPath = args[0];
        pidloop:

        for(int c = 1;c < args.length;c++) {
            String pid = args[c];
            String date, ext = "png";

            try {
                date = parse(pid);
            } catch(HttpResponseException e) {
                System.out.printf("E> Failed to get info, Error(Http %d)\n",
                                  e.getResponseCode());
                continue;
            } catch(IOException e) {
                System.out.println("E> Unknown Error...");
                e.printStackTrace();
                continue;
            }

            int i = 0;

            while(true) {
                byte[] img;

                try {
                    String url = String.format("http://i1.pixiv.net/img-original/img/%s/%s_p%d.%s",
                                   date, pid, i, ext);
                    System.out.printf("I> Downloading from %s\n", url);
                    img = getImg(date, pid, i, ext);
                } catch(HttpResponseException e) {
                    if(ext == "png" && i == 0) {
                        ext = "jpg";
                        continue;
                    } else {
                        continue pidloop;
                    }
                } catch(IOException e) {
                    System.out.println("E> Unknown Error...");
                    e.printStackTrace();
                    continue;
                }

                try {
                    String name = String.format("%s/%s_p%d.png", downloadPath, pid, i);
                    FileOutputStream f = new FileOutputStream(name);
                    f.write(img);
                    f.close();
                    System.out.printf("I> %s -> %s\n", pid, name);
                } catch(IOException e) {
                    System.out.printf("E> Failed to write to file, pid=%s\n", pid);
                    e.printStackTrace();
                    continue pidloop;
                }

                i++;
            }
        }
    }

    public static byte[] GET(String _url, String[][] header)
    throws HttpResponseException, IOException {
        HttpURLConnection conn = (HttpURLConnection)(new URL(_url)).openConnection();

        for(String[] prop : header) {
            conn.setRequestProperty(prop[0], prop[1]);
        }

        conn.connect();
        int status = conn.getResponseCode();

        if(status >= 300) {
            throw new HttpResponseException(status);
        }

        try(InputStream is = conn.getInputStream()) {
            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            byte[] data = new byte[65536];
            int nRead;

            while((nRead = is.read(data, 0, data.length)) != -1) {
                buffer.write(data, 0, nRead);
            }

            buffer.flush();
            return buffer.toByteArray();
        }
    }

    private static String parse(String pid)
    throws HttpResponseException, IOException {
        String host = "http://www.pixiv.net";
        String img_page = host + "/member_illust.php?mode=medium&illust_id=" + pid;
        String header[][] = {
            {"referer", host},
            {"Accept-Charset", host}
        };
        String res = new String(GET(img_page, header), "UTF-8");
        Pattern p = Pattern.compile(
                        "(?:class=\"img-container\"><a.*?><img src=\"(.*?)\"|" +
                        "class=\"sensored\"><img src=\"(.*?)\")");
        Matcher m = p.matcher(res);
        m.find();
        return m.group(0).replaceAll(".*/img/(.*)/.*$", "$1");
    }

    private static byte[] getImg(String date, String pid, int page, String ext)
    throws HttpResponseException, IOException {
        String url = String.format("http://i1.pixiv.net/img-original/img/%s/%s_p%d.%s",
                                   date, pid, page, ext);
        String header[][] = {{"referer", url}};
        return GET(url, header);
    }

}