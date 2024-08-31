import os
import platform
import subprocess
import sys
import zipfile

def install_jdk(platform, jdk_version = "17"): 
    if (platform == "linux"):
        try:
         install_jdk_on_linux(jdk_version)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
        install_maven_on_linux()
    if (platform == "windows"):
        try:
            if not os.path.exists(f"C:\Program Files\Java\jdk-{jdk_version}"):
                install_jdk_on_windows(jdk_version)
            install_maven_on_windows()
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

def install_jdk_on_windows(jdk_version):    
    jdk_url = f"https://download.oracle.com/java/{jdk_version}/latest/jdk-{jdk_version}_windows-x64_bin.exe"
    jdk_file = f"jdk-{jdk_version}_windows-x64_bin.exe"

    if not os.path.exists(jdk_file):
        subprocess.run(["curl", "-L", jdk_url, "-o", jdk_file])
        print(f"JDK descargado: {jdk_file}")
    else:
        print(f"El archivo {jdk_file} ya existe. Saltando descarga.")


    try:
        subprocess.run(["start", jdk_file], shell=True)
        print("Ejecutando instalador...")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el instalador: {e}")
    except FileNotFoundError:
        print("El archivo no se encontró o no se puede ejecutar.")

    # jdk_home = os.path.join("C:\\Program Files", f"Java\\jdk-{jdk_version}")
    # os.environ["JAVA_HOME"] = jdk_home
    # os.environ["PATH"] = f"{jdk_home}/bin:{os.environ['PATH']}"
    set_environment_variables(jdk_version)
    

def install_jdk_on_linux(jdk_version, linux_distro = "ubuntu"): 
    linux_distros = {
        "ubuntu": ["sudo", "apt", "install", f"openjdk-{jdk_version}-jdk"],
        "debian": ["sudo", "apt", "install", f"openjdk-{jdk_version}-jdk"],
        "fedora": ["sudo", "dnf", "install", f"java-{jdk_version}-openjdk-devel"]
    }
    if (linux_distro in linux_distros):
        subprocess.run(linux_distros[linux_distro], check=True)
        set_environment_variables(jdk_version)


def install_maven_on_windows(maven_version="3.8.8"):
    maven_url = f"https://dlcdn.apache.org/maven/maven-3/{maven_version}/apache-maven-{maven_version}-bin.zip"
    maven_file = f"apache-maven-{maven_version}-bin.zip"

    if not os.path.exists(maven_file):
        try:
            subprocess.run(["curl", "-L", maven_url, "-o", maven_file])
        except Exception as e:
            print(f"Error downloading Maven: {e}")
            return
    else:
        print(f"El archivo {maven_file} ya existe. Saltando descarga.")

    

    try:
        extract_zip(maven_file, f"C:\\Usuarios\{os.environ["USERPROFILE"]}\apache-maven-{maven_version}")
        # subprocess.run(["unzip", maven_file, "-d", f"apache-maven-{maven_version}-bin"])
    except Exception as e:
        print(f"Error unpacking Maven archive: {e}")
        return
    # subprocess.run(["curl", "-L", maven_url, "-o", maven_file])  

    # subprocess.run(["unzip", maven_file, "-d", f"apache-maven-{maven_version}"])


    maven_home = os.path.join(os.environ["USERPROFILE"], ".m2", f"apache-maven-{maven_version}")
    os.environ["MAVEN_HOME"] = maven_home
    os.environ["PATH"] = f"{maven_home}/bin:{os.environ['PATH']}"
    # maven_url = "https://dlcdn.apache.org/maven/maven-3.8.7/apache-maven-3.8.7-bin.zip"
    # maven_file = "apache-maven-3.8.7-bin.zip"
    # subprocess.run(["wget", maven_url, "-O", maven_file])

    # subprocess.run(["unzip", maven_file, "-d", "apache-maven-3.8.7"])

    # maven_home = "C:\\apache-maven-3.8.7"
    # os.environ["MAVEN_HOME"] = maven_home
    # os.environ["PATH"] = f"{maven_home}/bin:{os.environ['PATH']}"

def extract_zip(zip_file, destination):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destination)
    except zipfile.BadZipfile:
        print("El archivo ZIP está corrupto.")
    except FileNotFoundError:
        print("El archivo ZIP o la carpeta de destino no existe.")
    except PermissionError:
        print("No tienes permisos suficientes para descomprimir el archivo.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")



def install_maven_on_linux(): 
    sudo_apt_update_command = ["sudo", "apt", "update"]
    maven_linux_simple_install_commands = ["sudo", "apt", "install", "maven"]
    maven_version_command = ["mvn", "--version"]

    subprocess.run(sudo_apt_update_command, check=True)
    subprocess.run(maven_linux_simple_install_commands, check=True)
    subprocess.run(maven_version_command, check=True)
    maven_home = os.path.join(os.getcwd(), "apache-maven-3.8.7")
    os.environ["MAVEN_HOME"] = maven_home
    os.environ["PATH"] = f"{maven_home}/bin:{os.environ['PATH']}"


def set_environment_variables(jdk_version): 
    jdk_home = os.path.join(os.environ["HOME"], ".jdks", f"jdk-{jdk_version}")
    os.environ["JAVA_HOME"] = jdk_home
    os.environ["PATH"] = f"{jdk_home}/bin:{os.environ['PATH']}"    

def main():
    platformToLowerCase = platform.system().lower()
    install_jdk(platformToLowerCase)

main()