import os
import platform
import subprocess
import sys
import zipfile

def install_jdk(platform, jdk_version = "17", maven_version="3.8.8"): 
    if (platform == "linux"):
        try:
         install_jdk_on_linux(jdk_version)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
        install_maven_on_linux()
    if (platform == "windows"):
        try:
            if not os.path.exists(f"C:\\Program Files\\Java\\jdk-{jdk_version}"):
                install_jdk_on_windows(jdk_version)
            if not os.path.exists(f"C:\\Program Files\\apache-maven\\apache-maven-{maven_version}"): 
                install_maven_on_windows()
            set_environment_variables_on_windows(jdk_version, maven_version)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

def install_jdk_on_windows(jdk_version):    
    jdk_url = f"https://download.oracle.com/java/{jdk_version}/latest/jdk-{jdk_version}_windows-x64_bin.exe"
    jdk_file = f"jdk-{jdk_version}_windows-x64_bin.exe"

    if not os.path.exists(jdk_file):
        subprocess.run(["curl", "-L", jdk_url, "-o", jdk_file])
        print(f"JDK downloaded: {jdk_file}")
    else:
        print(f"the file {jdk_file} all ready exist. Skip download.")


    try:
        subprocess.run(["start", jdk_file], shell=True)
        print("Running installer...")
    except subprocess.CalledProcessError as e:
        print(f"Error running the installer: {e}")
    except FileNotFoundError:
        print("The file was not found or cannot be executed.")

    # jdk_home = os.path.join("C:\\Program Files", f"Java\\jdk-{jdk_version}")
    # os.environ["JAVA_HOME"] = jdk_home
    # os.environ["PATH"] = f"{jdk_home}/bin:{os.environ['PATH']}"
    
    

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
    maven_url = f"https://dlcdn.apache.org/maven/maven-3/{maven_version}/binaries/apache-maven-{maven_version}-bin.zip"
    maven_file = f"apache-maven-{maven_version}-bin.zip"

    if not os.path.exists(maven_file):
        try:
            subprocess.run(["curl", "-L", maven_url, "-o", maven_file])
            print(f"Maven downloaded: {maven_file}")
        except Exception as e:
            print(f"Error downloading Maven: {e}")
            return
    else:
        print(f"the file {maven_file} all ready exist. Skip download.")

    

    try:
        extract_zip(maven_file, f"C:\\Program Files\\apache-maven\\apache-maven-{maven_version}")
        # subprocess.run(["unzip", maven_file, "-d", f"apache-maven-{maven_version}-bin"])
    except Exception as e:
        print(f"Error unpacking Maven archive: {e}")
        return
    # subprocess.run(["curl", "-L", maven_url, "-o", maven_file])  

    # subprocess.run(["unzip", maven_file, "-d", f"apache-maven-{maven_version}"])

    # exixst_maven_home = False
    # if exixst_maven_home == True:
    #     maven_home = f"C:\\Program Files\\apache-maven\\apache-maven-{maven_version}"
    #     # os.environ["MAVEN_HOME"] = maven_home
    #     # os.environ["PATH"] = f"{maven_home}/bin:{os.environ['PATH']}"
    #     maven_home_set_command = ["setx", "MAVEN_HOME", maven_home]
    #     path_update_command = ["setx", "PATH", f"{maven_home}/bin;%{os.environ['PATH']}"]


    # try:
    #     subprocess.run(maven_home_set_command, check=True)
    #     subprocess.run(path_update_command, check=True)
    #     print("Variables de entorno establecidas con éxito.")
    # except subprocess.CalledProcessError as e:
    #     print(f"Error al establecer las variables de entorno: {e}")
    # maven_url = "https://dlcdn.apache.org/maven/maven-3.8.7/apache-maven-3.8.7-bin.zip"
    # maven_file = "apache-maven-3.8.7-bin.zip"
    # subprocess.run(["wget", maven_url, "-O", maven_file])

    # subprocess.run(["unzip", maven_file, "-d", "apache-maven-3.8.7"])

    # maven_home = "C:\\apache-maven-3.8.7"
    # os.environ["MAVEN_HOME"] = maven_home
    # os.environ["PATH"] = f"{maven_home}/bin:{os.environ['PATH']}"




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


def set_environment_variables_on_windows(jdk_version, maven_version): 
        # java environment variables config
        jdk_home = f"C:\\Program Files\\Java\\jdk-{jdk_version}"
        java_home_set_command = ["setx", "JAVA_HOME", jdk_home]
        path_update_java_command = ["setx", "PATH", f"{jdk_home}/bin;%{os.environ['PATH']}"]
        # maven environment variables config
        maven_home = f"C:\\Program Files\\apache-maven\\apache-maven-{maven_version}"
        maven_home_set_command = ["setx", "MAVEN_HOME", maven_home]
        path_update_maven_command = ["setx", "PATH", f"{maven_home}/bin;%{os.environ['PATH']}"]

        try:
            subprocess.run(java_home_set_command, check=True)
            subprocess.run(path_update_java_command, check=True)
            subprocess.run(maven_home_set_command, check=True)
            subprocess.run(path_update_maven_command, check=True)
            print("Environment variables set successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error setting environment variables: {e}")

def extract_zip(zip_file, destination):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destination)
    except zipfile.BadZipfile:
        print("The ZIP file is corrupted.")
    except FileNotFoundError:
        print("The ZIP file or the destination folder does not exist.")
    except PermissionError:
        print("You do not have sufficient permissions to unzip the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
def main():
    platformToLowerCase = platform.system().lower()
    install_jdk(platformToLowerCase)

main()