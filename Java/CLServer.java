import java.io.File;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;
import java.security.Permission;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.MalformedURLException;
import java.net.ServerSocket;
import java.net.Socket;

public class CLServer {
   private static final int PORT = 8080;
   static final PrintStream _out = System.out;
   static final PrintStream _err = System.err;
   static ClassLoader cl;
   static final boolean DEBUG = true;

   public static void debug(String message) {
      if (DEBUG) {
         _out.print("D> ");
         _out.println(message);
      }
   }

   public static void error(String message) {
      _out.print("E> ");
      _out.println(message);
   }

   public static void info(String message) {
      _out.print("I> ");
      _out.println(message);
   }

   public static void main(String[] args) throws NoSuchMethodException, SecurityException, IllegalAccessException,
         IllegalArgumentException, InvocationTargetException, IOException {
      System.setSecurityManager(new SecurityManager() {
         @Override
         public void checkExit(int status) {
            throw new RuntimeException("Blocking System.exit();");
         }

         @Override
         public void checkPermission(Permission p) {

         }
      });

      cl = URLClassLoader.newInstance(new URL[] {}, CLTest.class.getClassLoader());
      addURL(".");

      try (ServerSocket server = new ServerSocket(PORT)) {
         info("Server is listening " + PORT);

         while (true) {
            try {
               try {
                  Socket s = server.accept();
                  handleSocket(s);
               } catch (IOException e) {
                  System.setOut(_out);
                  System.setErr(_err);
                  e.printStackTrace();
               } finally {
                  System.setOut(_out);
                  System.setErr(_err);
               }
            } catch (Error | Exception e) {
               debug("continue anyway");
            }
         }
      }
   }

   public static void handleSocket(Socket s) throws IOException {
      InputStream is = s.getInputStream();
      PrintStream out = new PrintStream(s.getOutputStream());
      BufferedReader in = new BufferedReader(new InputStreamReader(is));

      System.setOut(out);
      System.setErr(out);
      try {
         handleCommand(in, out);
      } finally {
         out.flush();
         System.setOut(_out);
         System.setErr(_err);
         in.close();
         out.close();
         is.close();
         s.close();
      }
   }

   public static void handleCommand(BufferedReader in, PrintStream out) throws IOException {
      debug("Packet: ");
      String cmd = in.readLine();
      if (cmd.equals("#cp")) {
         debug("#cp");
         String data = in.readLine();
         debug(data);
         try {
            CLTest.addURL(data);
         } catch (Error | Exception e) {
            e.printStackTrace(out);
         }
      } else if (cmd.equals("#run")) {
         debug("#run");
         ArrayList<String> cps = new ArrayList<String>();
         String name = null;
         ArrayList<String> args = new ArrayList<String>();
         // 0 for cp, 1 for name, 2 for args
         int state = 0;
         String line;
         while ((line = in.readLine()) != null && line.length() > 0) {
            debug(line);
            if (line.equals("#cp")) {
               state = 0;
            } else if (line.equals("#name")) {
               state = 1;
            } else if (line.equals("#args")) {
               state = 2;
            } else {
               switch (state) {
               case 0:
                  cps.add(line);
                  break;
               case 1:
                  name = line;
                  break;
               case 2:
                  args.add(line);
               }
            }
         }
         if (name != null) {
            CLTest.callMain(addTempURL(cps.toArray(new String[] {})), name, args.toArray(new String[] {}), out);
         } else {
            out.println("E> Missing class name");
            error("Missing class name");
         }
      }
      debug("End Packet");
   }

   public static void addURL(String s) throws NoSuchMethodException, SecurityException, IllegalAccessException,
         IllegalArgumentException, InvocationTargetException, MalformedURLException {
      Method method = URLClassLoader.class.getDeclaredMethod("addURL", new Class[] { URL.class });

      File f = new File(s);

      method.setAccessible(true);
      info("Adding " + s);
      method.invoke(cl, new Object[] { f.toURI().toURL() });
   }

   public static ClassLoader addTempURL(String[] s) throws MalformedURLException {

      ClassLoader newCl = URLClassLoader.newInstance(Arrays.stream(s).map(x -> {
         try {
            info("Adding temp url" + x);
            return new File(x).toURI().toURL();
         } catch (MalformedURLException e) {
            throw new RuntimeException(e);
         }
      }).collect(Collectors.toList()).toArray(new URL[] {}), cl);
      return newCl;
   }

   public static void callMain(String className, String[] args, PrintStream out) {
      callMain(cl, className, args, out);
   }

   public static void callMain(ClassLoader cl, String className, String[] args, PrintStream out) {
      try {
         info("Running " + className);
         cl.loadClass(className).getMethod("main", String[].class).invoke(null, (Object) args);
      } catch (InvocationTargetException e) {
         e.getCause().printStackTrace(out);
      } catch (Error | Exception e) {
         e.printStackTrace(out);
      }
   }
}
