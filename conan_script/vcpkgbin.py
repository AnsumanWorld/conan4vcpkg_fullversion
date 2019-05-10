import os,platform,sys,time,yaml
from colorama import init,Fore
import vcpkg_mgr
import conan_mgr
from conans import tools
init(autoreset=True)

class Vcpkgbin:
    _user_type="help"
    _valid_arg_status = False
    _vcpkg_path =os.path.normpath(os.getcwd())
    _port=[]
    _triplet=""
    _repository=""
    _no_package_in_server=False

    def __init__(self):
        self._user_type="help"
        self.validate_arg()
        if self._valid_arg_status == True:
            self._vcpkg = vcpkg_mgr.vcpkg_mgr(self._vcpkg_path)
            self._conan = conan_mgr.conan_mgr()

    def print_message(self,input_str,type="",term='\n'):
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'

        if type.lower() == 'warning':
            print(YELLOW + input_str,end=term)
        elif type.lower() == 'error':
            print(RED + input_str,end=term)
        elif type.lower() == 'success':
            print(GREEN + input_str,end=term)
        else:
            print(input_str,end=term)

    def help(self,info_type):
        if "help" in info_type:
            print("commands:")
            print("vcpkgbin download     downloading particular package")
            print("vcpkgbin upload       uploading all installed package in the remote")
            print("vcpkgbin install      installing and packaging particular port for uploading")            
            print("vcpkgbin remove       remove particular package or port")
            print("vcpkgbin search       search particular package in local or remote")
            print("vcpkgbin help topics  display list of help topics")
        elif "download" in info_type:
            print("vcpkgbin download <remote repository name> <port name> <triplet>")
            print("         - for downloading particular package")
        elif "install" in info_type:
            print("vcpkgbin install <remote repository name> <port name> <triplet>")
            print("         - - for installing,packaging and uploading particular port and its dependencies to server")
        elif "install_only" in info_type:
            print("vcpkgbin install_only <remote repository name> <port name> <triplet>")
            print("         - - for installing,packaging and uploading particular port to server")
        elif "upload" in info_type:
            print("vcpkgbin upload <remote repository name>")
            print("         - for uploading all installed package present in current vcpkg in the remote")
        elif "upload_only" in info_type:
            print("vcpkgbin upload_only <remote repository name>")
            print("         - for uploading all installed package present in local server in the remote")
        elif "remove" in info_type:
            print("vcpkgbin remove <local/remote> <remote repository name>")
            print("         - for removing particular repository from the local or remote")
            print("vcpkgbin remove <local/remote> <remote repository name> <port name> <triplet>")
            print("         - for removing particular port from the local or remote")
        elif "list" in info_type:
            print("vcpkgbin list local")
            print("         - search for repository installed in local")
            print("vcpkgbin list local <triplet>")
            print("         - search for port installed in local")
            print("vcpkgbin list local <triplet> <port>")
            print("         - search ports of particular triplet installed in local")
            print("vcpkgbin list remote <remote repository name>")
            print("         - search for all packages of the particular repository installed in remote")
            print("vcpkgbin list remote <remote repository name> <triplet>")
            print("         - search for all the ports of the particular triplet of the particular repository in remote")
            print("vcpkgbin list remote <remote repository name> <port name>")
            print("         - search for port information of the particular port name of particular repository in remote")
            print("vcpkgbin list remote <remote repository name> <port name> <triplet>")
            print("         - search for port information of the particular portname and triplet of particular repository in remote")

    def validate_arg(self):
        argc = len(sys.argv)
        if argc >= 2:
            self._user_type = sys.argv[1]
            if "install" in self._user_type:
                if argc == 5:
                    self._repository=sys.argv[2]
                    self._port=sys.argv[3].split(" ")
                    self._triplet=sys.argv[4]
                    self._valid_arg_status = True
            elif "install_only" in self._user_type:
                if argc == 5:
                    self._repository=sys.argv[2]
                    self._port=sys.argv[3].split(" ")
                    self._triplet=sys.argv[4]
                    self._valid_arg_status = True
            elif "download" in self._user_type:
                if argc == 5:
                    self._repository=sys.argv[2]
                    self._port=sys.argv[3].split(" ")
                    self._triplet=sys.argv[4]
                    self._valid_arg_status = True
            elif "upload" in self._user_type:
                if  argc == 3:
                    self._repository=sys.argv[2]
                    self._valid_arg_status = True
            elif "upload_only" in self._user_type:
                if  argc == 3:
                    self._repository=sys.argv[2]
                    self._valid_arg_status = True
            elif "remove" in self._user_type:
                if argc == 4:
                    self._repository=sys.argv[3]
                    self._valid_arg_status = True
                elif argc == 6:
                    self._repository=sys.argv[3]
                    self._port=sys.argv[4].split(" ")
                    self._triplet=sys.argv[5]
                    self._valid_arg_status = True
            elif "list" in self._user_type:
                if "local" == sys.argv[2]:
                    if argc == 3:
                        self._valid_arg_status = True
                    elif argc == 4:
                        self._triplet=sys.argv[3]
                        self._valid_arg_status = True
                    elif argc == 5:   
                        self._triplet=sys.argv[3]
                        self._port=sys.argv[4].split(" ")
                        self._valid_arg_status = True
                elif "remote" == sys.argv[2]:
                    if argc == 4:
                        self._repository=sys.argv[3]
                        self._valid_arg_status = True
                    elif argc == 5:
                        self._repository=sys.argv[3]
                        self._triplet=sys.argv[4]
                        self._valid_arg_status = True
                    elif argc == 6:
                        self._repository=sys.argv[3]
                        self._triplet=sys.argv[4]
                        self._port=sys.argv[5].split(" ")
                        self._valid_arg_status = True
            elif "help" in self._user_type:
                if argc== 3:
                    self.help(sys.argv[2])
                    self._valid_arg_status = True
            else:
                self._user_type = "help"
        else:
            self._valid_arg_status = False

        if self._valid_arg_status == False:
             self.help(self._user_type)

        if self._user_type == "install" or self._user_type == "install_only" or self._user_type == "upload" or self._user_type == "upload_only":
            if self.validate_uploading() == False:
                self._valid_arg_status = False

    def validate_uploading(self):
        status=True
        if os.environ['VCPKG_USERNAME'] == "NOT_YET_SET" and os.environ['VCPKG_API_KEY'] == "NOT_YET_SET":
            self.print_message("user name and api key is not set to upload!!!","error")
            self.print_message("please set user name and api key in vcpkgbin.bat","warning")
            status=False
        return status

    def run(self):
        if self._valid_arg_status == True:
            if sys.argv[2] != "local":
                print("configuring conan please wait")
                self._conan.init_conan_setting()
                print("configuring conan completed")
            if self._user_type == "install":
                self.install()
            if self._user_type == "install_only":
                self.install_only()
            elif self._user_type == "upload":
                self.upload()
            elif self._user_type == "upload_only":
                self.upload_only()
            elif self._user_type == "download":
                self.download()
            elif self._user_type == "remove":
                self.remove()
            elif self._user_type == "list":
                self.list()

    def install(self):
        dependant_port_list=[]
        for port in self._port:
            retcode = self._vcpkg.run("install %s:%s" % (port,self._triplet))
            if port not in dependant_port_list:
                dependant_port_list.extend(self._vcpkg.get_dependant_port(port))
        vcpkg_package_list=[]        
        for port in dependant_port_list:
            vcpkg_package_list.append(port+":"+self._triplet) 
        self.init_upload()
        self.make_conan_pkg(vcpkg_package_list) 
        conan_pkg_id_list=self.update_conan_pkg_info(self._repository,vcpkg_package_list)        
        self.upload_conan_pkg(self._repository,conan_pkg_id_list)

    def install_only(self):
        vcpkg_package_list=[]
        for port in self._port:
            retcode = self._vcpkg.run("install %s:%s" % (port,self._triplet))
            vcpkg_package_list.append(port+":"+self._triplet)
        if len(vcpkg_package_list) != 0:
            self.make_conan_pkg(vcpkg_package_list)            
            conan_pkg_id_list=self.update_conan_pkg_info(self._repository,vcpkg_package_list)
            self.upload_conan_pkg(self._repository,conan_pkg_id_list)

    def upload(self):
        vcpkg_package_list=self._vcpkg.get_installed_pkg_list()
        self.make_conan_pkg(vcpkg_package_list)
        conan_pkg_id_list=self.update_conan_pkg_info(self._repository,vcpkg_package_list)
        self.upload_conan_pkg(self._repository,conan_pkg_id_list)

    def upload_only(self):
        ret_code=self._conan.upload(self._repository,"",True)

    def update_conan_pkg_info(self,repo,req_vcpkg_list):
        conan_pkg_info=self.download_conan_pkg_info()
        temp_folder = self._vcpkg_path + os.sep+"Temp"
        pkg_info_file=temp_folder+ os.sep+ "packagelist.yml"
        info_pkg_found=False
        conan_pkg_list=self._conan.get_installed_pkg_data(temp_folder,repo)
        conan_pkg_id_list=[]
        dependant_vcpkg_data={}
        if len(conan_pkg_list) !=0:
            vcpkg_list,installed_vcpkg_data =self._vcpkg.get_installed_pkg_data()
            if len(vcpkg_list) !=0:
                for req_pkg in req_vcpkg_list:
                    for conan_pkg in conan_pkg_list:
                        conan_pkg_id,conan_pkg_port,conan_pkg_triplet=conan_pkg.split(":")
                        port,triplet=req_pkg.split(":")
                        if port == conan_pkg_port and conan_pkg_triplet==triplet:
                            if 'local' in installed_vcpkg_data.keys() and triplet in installed_vcpkg_data['local'].keys() and port in installed_vcpkg_data['local'][triplet].keys():
                                conan_pkg_id_list.append(conan_pkg)
                                depend_vcpkg_list = self._vcpkg.get_dependant_port(port)   
                                pkg_id_data={"Package_ID":conan_pkg_id}
                                depend_vcpkg_list.remove(port)
                                dependant_vcpkg_data={"Dependant":depend_vcpkg_list}
                                data = installed_vcpkg_data['local'][triplet][port]
                                pkg_data= {**data,**pkg_id_data,**dependant_vcpkg_data}
                                conan_pkg_info=self._vcpkg.update_package_info(repo,port,triplet,pkg_data,conan_pkg_info)
                        elif conan_pkg_port=="info" and conan_pkg_triplet=="info" and info_pkg_found==False:
                            conan_pkg_id_list.append(conan_pkg)
                            info_pkg_found = True
                self.write_data_to_yml(pkg_info_file,conan_pkg_info)
                self.make_conan_pkg_info()

            if info_pkg_found ==False:
                conan_pkg_list=self._conan.get_installed_pkg_data(temp_folder,repo)
                for conan_pkg in conan_pkg_list:
                    conan_pkg_id,conan_pkg_port,conan_pkg_triplet=conan_pkg.split(":")
                    if conan_pkg_port=="info" and conan_pkg_triplet=="info":
                        conan_pkg_id_list.append(conan_pkg)

        return conan_pkg_id_list

    def upload_conan_pkg(self,repo,conan_pkg_id_list):        
        print("===============================================================")
        if self._no_package_in_server == True:
            ret_code=self._conan.upload(repo,"",True)
        else:
            index = 1
            total_package=len(conan_pkg_id_list)            
            for conan_pkg in conan_pkg_id_list:
                conan_pkg_id,conan_pkg_port,conan_pkg_triplet=conan_pkg.split(":")
                if conan_pkg_port!="info" and conan_pkg_triplet!="info":
                    package_msg = conan_pkg_port+":"+conan_pkg_triplet
                else:
                    package_msg = "package information"
                self.print_message("uploading %s/%s: %s please wait" % (index,total_package,package_msg),"success",'\r')

                ret_code=self._conan.upload(repo,conan_pkg_id,True)

                if ret_code == 0:
                    self.print_message("uploading %s/%s: %s is completed      " % (index,total_package,package_msg),"success")
                else:
                    self.print_message("uploading %s/%s: %s is failed     " % (index,total_package,package_msg),"error")

                index+=1
        print("===============================================================")

    def init_upload(self):
        self._conan.remove('local',self._repository)
        upload_package_info_recipe_template_file = self._vcpkg_path + os.sep + "conan_script" + os.sep + "conan_upload_recipe_templete.py"
        upload_package_info_recipe_gen_dir= self._vcpkg_path + os.sep + "temp"
        self._conan.make_upload_recipe(upload_package_info_recipe_template_file,upload_package_info_recipe_gen_dir,self._repository,"packagelist.yml",upload_package_info_recipe_gen_dir)
        self._conan.export(upload_package_info_recipe_gen_dir,self._repository)
        self._conan.upload(self._repository,"",True)

    def make_conan_pkg(self,installed_list):
        index = 1
        total_package=len(installed_list)        
        print("===============================================================")
        for package in installed_list:
            self.print_message("packaging %s/%s: %s please wait..." % (index,total_package,package),"success",'\r')
            port,triplet=package.split(":")
            self._vcpkg.make_conan_pkg(port,triplet)
            upload_recipe_template_file = self._vcpkg_path + os.sep + "conan_script" + os.sep + "conan_upload_recipe_templete.py"
            upload_recipe_gen_dir= self._vcpkg_path + os.sep + "Temp"
            self._conan.updatesetting("vcpkg_port",[port],"vcpkg_triplet",[triplet])
            upload_vcpkg_binary_dir= upload_recipe_gen_dir + os.sep + "uploaded"
            vcpkg_port_package_7z = port+"_"+triplet+".7z"
            self._conan.make_upload_recipe(upload_recipe_template_file,upload_recipe_gen_dir,self._repository,vcpkg_port_package_7z,upload_vcpkg_binary_dir)
            self._conan.create(upload_recipe_gen_dir,self._repository,port,triplet)
            conan_mgr.system('del /Q %s\*.py' % upload_recipe_gen_dir)
            self.print_message("packaging %s/%s: %s is completed       " % (index,total_package,package),"success")
            index+=1
        print("===============================================================")

    def make_conan_pkg_info(self):        
        upload_package_info_recipe_template_file = self._vcpkg_path + os.sep + "conan_script" + os.sep + "conan_upload_recipe_templete.py"
        upload_package_info_recipe_gen_dir= self._vcpkg_path + os.sep + "temp"
        self._conan.make_upload_recipe(upload_package_info_recipe_template_file,upload_package_info_recipe_gen_dir,self._repository,"packagelist.yml",upload_package_info_recipe_gen_dir)
        self._conan.create(upload_package_info_recipe_gen_dir,self._repository,"info","info")
        os.system('del /Q %s\*.py' % upload_package_info_recipe_gen_dir)

    def download_conan_pkg_info(self):
        remote_installed_data={}
        download_recipe_template_file = self._vcpkg_path + os.sep + "conan_script" + os.sep + "conan_download_recipe_template.txt"
        download_recipe_gen_dir= self._vcpkg_path + os.sep + "Temp"
        package_info_file=download_recipe_gen_dir+ os.sep+ "packagelist.yml"
        if os.path.isfile(package_info_file )==True:
            os.system('del /Q %s' % package_info_file)
        self._conan.make_download_recipe(download_recipe_template_file,download_recipe_gen_dir,self._repository,".")
        ret_code=self._conan.download(download_recipe_gen_dir,download_recipe_gen_dir,"info","info")
        if ret_code!=0:
            self._no_package_in_server=True
        else:
            status,remote_installed_data=self._conan.getdata_from_yml(package_info_file)        
        return remote_installed_data

    def download_conan_pkg(self,repo,port,triplet):
        download_recipe_template_file = self._vcpkg_path + os.sep + "conan_script" + os.sep + "conan_download_recipe_template.txt"
        download_recipe_gen_dir= self._vcpkg_path + os.sep + "Temp"
        retcode=self._conan.make_download_recipe(download_recipe_template_file,temp_folder,repo,".")
        if retcode == 0:
            retcode=self._conan.download(temp_folder,temp_folder,port,triplet)
        return retcode

    def download(self):
        retcode = 0
        download_recipe_template_file = self._vcpkg_path + os.sep + "conan_script" + os.sep + "conan_download_recipe_template.txt" 
        installed_pkg_count=0
        conan_pkg_info=self.download_conan_pkg_info()
        if len(conan_pkg_info) != 0:
            for d_port in self._port:
                installed_pkg_list=self._vcpkg.get_installed_pkg_list()
                req_vcpkg_port_list=[]
                if self._repository in conan_pkg_info.keys() and self._triplet in conan_pkg_info[self._repository].keys() and d_port in conan_pkg_info[self._repository][self._triplet].keys() and 'Dependant' in conan_pkg_info[self._repository][self._triplet][d_port].keys():
                    req_vcpkg_port_list.append(d_port)
                    req_vcpkg_port_list.extend(conan_pkg_info[self._repository][self._triplet][d_port]['Dependant'])
                    self._conan.updatesetting("vcpkg_port",req_vcpkg_port_list,"vcpkg_triplet",[self._triplet])
                    for package in installed_pkg_list:
                        installed_port,installed_triplet=package.split(":")
                        if installed_port in req_vcpkg_port_list and installed_triplet == self._triplet:
                            req_vcpkg_port_list.remove(installed_port)

                    if len(req_vcpkg_port_list) == 0:
                        continue
                    index = 1
                    total_package=len(req_vcpkg_port_list) 
                    print("===============================================================")
                    for port in req_vcpkg_port_list:
                        self.print_message("downloading %s/%s: %s:%s please wait" % (index,total_package,port,self._triplet),"success",'\r')
                        retcode = self.download_conan_pkg(self._repository,port,self._triplet)
                        if retcode == 0:
                            self.print_message("downloading %s/%s: %s:%s is completed               " % (index,total_package,port,self._triplet),"success")
                            print("--configuring %s/%s: %s:%s Please wait..." % (index,total_package,port,self._triplet),end='\r')
                            status = self._vcpkg.load_conan_pkg(temp_folder,port,self._triplet) 
                            if status == True:
                                installed_pkg_count+=1
                                print("--configuring %s/%s: %s:%s is completed       " % (index,total_package,port,self._triplet))
                                self._vcpkg.update_installed_vcpkg(self._repository,[port],self._triplet,conan_pkg_info)
                            else:
                                print("--configuring %s/%s: %s:%s is failed          " % (index,total_package,port,self._triplet))
                        else:
                            self.print_message("fail to download %s/%s: %s:%s           " % (index,total_package,port,self._triplet),"error")
                        index+=1
                    print("===============================================================")
                else:
                    self.print_message("%s:%s not available in server" % (d_port,self._triplet),"error")
        else:
            self.print_message("no package available in server","error")

    def remove_remote(self):
        remove_all=False
        if len(self._port) != 0 and self._triplet != "":
            conan_pkg_data=self.download_conan_pkg_info()
            print(conan_pkg_data)
            if len(conan_pkg_data) !=0:
                for port in self._port:
                    if self._repository in conan_pkg_data.keys() and self._triplet in conan_pkg_data[self._repository].keys() and port in conan_pkg_data[self._repository][self._triplet].keys() and 'Package_ID' in conan_pkg_data[self._repository][self._triplet][port].keys():
                        package_id = conan_pkg_data[self._repository][self._triplet][port]['Package_ID']
                        retcode=self._conan.remove('remote',self._repository,package_id)
                        if retcode==0:
                            print("%s %s:%s is removed successfully" % (self._repository,port,self._triplet) )
                            del conan_pkg_data[self._repository][self._triplet][port]
                            if len(conan_pkg_data[self._repository][self._triplet]) == 0:
                                del conan_pkg_data[self._repository][self._triplet]
                                if len(conan_pkg_data[self._repository]) == 0:
                                    del conan_pkg_data[self._repository]
                                    self._conan.remove('remote',self._repository)
                                    remove_all=True
                                    break
                        else:
                             print("%s %s:%s is not removed successfully" % (self._repository,port,self._triplet) )
                if remove_all==False:
                    package_info_file=self._vcpkg_path + os.sep + "Temp"+ os.sep+ "packagelist.yml"
                    self.write_data_to_yml(package_info_file,conan_pkg_data)
                    self._conan.remove('local',self._repository)
                    self.make_conan_pkg_info()
                    self._conan.upload(self._repository,"",True)               
        else:
            retcode=self._conan.remove('remote',self._repository)
            if retcode==0:
                print("%s is removed successfully" % self._repository)
            else:
                print("%s:%s is not removed successfully" % (port,self._triplet) )

    def remove_local(self):
        if len(self._port) != 0 and self._triplet != "":
            for port in self._port:
                if len(conan_pkg_data) !=0:
                    retcode=self._vcpkg.run("remove %s:%s --recurse" % (port,self._triplet))
                    if retcode==0:
                        print("%s:%s is removed successfully" % (port,self._triplet) )
                    else:
                        print("%s:%s is not removed successfully" % (port,self._triplet) )
        else:
            vcpkg_list,installed_vcpkg_data =self._vcpkg.get_installed_pkg_data()
            for pkg in vcpkg_list:
                port,triplet=pkg.split(":")
                retcode=self._vcpkg.run("remove %s:%s --recurse" % (port,triplet))
                if retcode==0:
                    print("%s:%s is removed successfully" % (port,self._triplet) )
                else:
                    print("%s:%s is not removed successfully" % (port,self._triplet) )

    def remove(self):
        if sys.argv[2] == "remote":
            self.remove_remote()
        elif sys.argv[2] == "local":
            self.remove_local()
        else:
            print("wrong remove command")

    def write_data_to_yml(self,filename,data):
        with open(filename, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style = False)

    def show_pkg(self,repo,triplet,port_list,pkg_data):
        if len(pkg_data) != 0:
            if triplet != "" and len(port_list) != 0 and repo in pkg_data.keys() and triplet in pkg_data[repo].keys():
                self.print_message(repo,"success")
                self.print_message("  " + triplet,"success")
                for port in port_list:
                    if port in pkg_data[repo][triplet].keys():
                        self.print_message("    " + port,"success")
                        for tag in pkg_data[repo][triplet][port]:
                            value = "      "+str(tag) +": "+ str(pkg_data[repo][triplet][port][tag])
                            self.print_message(value,"success")
            elif triplet!="" and len(port_list) == 0 and repo in pkg_data.keys() and triplet in pkg_data[repo].keys():
                    self.print_message(repo,"success")
                    self.print_message("  " + triplet,"success")
                    for tag in pkg_data[repo][triplet]:
                        value = "    "+str(tag)
                        self.print_message(value,"success")
            elif repo!="" and triplet=="" and len(port_list) == 0 and repo in pkg_data.keys():
                    self.print_message(repo,"success")
                    for tag in pkg_data[repo]:
                        value = "  "+str(tag)
                        self.print_message(value,"success")
            else:
                self.print_message("no entry found","error")
        else:
            self.print_message("no package found","error")

    def list(self):
        installed_port=[]
        if sys.argv[2] == "local":
            installed_port,installed_port_data =self._vcpkg.get_installed_pkg_data()
            self.show_pkg("local",self._triplet,self._port,installed_port_data)
        elif sys.argv[2] == "remote":
            print("collecting information from remote,please wait")
            conan_pkg_info=self.download_conan_pkg_info()
            self.show_pkg(self._repository,self._triplet,self._port,conan_pkg_info)

if __name__ == "__main__":
    os.system('echo "%s" > vcpkgbin.log' % sys.argv[0:])
    vcpkgbin_mgr=Vcpkgbin()
    temp_folder = vcpkgbin_mgr._vcpkg_path + os.sep+"Temp"
    os.makedirs(temp_folder, exist_ok=True)
    vcpkgbin_mgr.run()    
    os.system('rmdir /Q /S %s' % temp_folder)