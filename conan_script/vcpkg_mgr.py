import os,platform,sys,time,yaml
from conans import tools

class vcpkg_mgr:
    def __init__(self,vcpkg_root):
        self._vcpkg_root=vcpkg_root

    def run(self,command):
        vcpkg_tool = self._vcpkg_root + os.sep + "vcpkg.exe"
        retcode=os.system('%s %s' % (vcpkg_tool,command))
        os.system('%s list > nul' % (vcpkg_tool))
        return retcode

    def make_conan_pkg(self,port,triplet):
        port_package = "%s_%s" % (port,triplet)
        vcpkg_uploaded_dir= self._vcpkg_root + os.sep +"Temp"+os.sep+ "uploaded"+ os.sep 
        vcpkg_uploaded_file = vcpkg_uploaded_dir+port_package+".7z"
        vcpkg_port_package_dir = self._vcpkg_root + os.sep + "packages" + os.sep +port+"_"+ triplet+ os.sep +"*"
        vcpkg_port_package_lst_file = self._vcpkg_root + os.sep + "installed"+os.sep+"vcpkg"+os.sep+"info" + os.sep +port+"_*_"+triplet+".list"
        vcpkg_port_package = self._vcpkg_root + os.sep + "packages" + os.sep +port_package+ os.sep +"*"
        compress_command = "7z.exe a "+vcpkg_uploaded_file+" "+ vcpkg_port_package_dir
        system(compress_command)
        compress_command1 = "7z.exe a "+vcpkg_uploaded_file+" "+ vcpkg_port_package_lst_file
        system(compress_command1)

    def load_conan_pkg(self,download_pkg_dir,port,triplet):
        status = False
        download_pkg_file = download_pkg_dir+os.sep+ "%s_%s.7z" % (port,triplet)
        install_dir= self._vcpkg_root+os.sep+"installed"+os.sep+triplet+os.sep
        package_install_dir= self._vcpkg_root+os.sep+"packages"+os.sep+"%s_%s" % (port,triplet)+os.sep
        vcpkg_port_package_list_dir = self._vcpkg_root + os.sep + "installed"+os.sep+"vcpkg"+os.sep+"info" + os.sep
        vcpkg_port_installed_lst_file = install_dir +port+"_*_"+triplet+".list"
        if os.path.isfile(download_pkg_file )==True:
            system('7z.exe x %s -aoa -o%s' % (download_pkg_file,package_install_dir))
            system('7z.exe x %s -aoa -o%s' % (download_pkg_file,install_dir))
            system('del /Q %sCONTROL' % install_dir)
            system('del /Q %sBUILD_INFO' % install_dir)            
            os.makedirs(vcpkg_port_package_list_dir, exist_ok=True)
            system('copy /Y %s %s' % (vcpkg_port_installed_lst_file,vcpkg_port_package_list_dir))
            system('del /Q %s%s*.list' % (install_dir,port))
            system('del /Q %s%s*.list' % (package_install_dir,port))
            status = True
        return status

    def remove(self,port,triplet):
        self.run("remove %s:%s" % (port,triplet))
        port_package = "%s_%s" % (port,triplet)
        vcpkg_uploaded_file= self._vcpkg_root + os.sep + "uploaded" + os.sep+ port_package+".7z"
        os.system('del /Q %s' % vcpkg_uploaded_file)

    def parse_portlist(self,port_control_str):
        startindex = 0
        endindex = -1
        port_list = []
        port_str_list = port_control_str.split(",")
        for port_str in port_str_list:
            port = " ".join(port_str.split())
            findindex = port.find("(")
            if findindex == -1:
                findindex = len(port)
            else:
                findindex -=1
            port_list.append(port[0:findindex])
        return port_list

    def read_port_from_control(self,port):
        port_list=[]
        portfile=self._vcpkg_root + os.sep+"ports"+ os.sep+str(port)+os.sep+"CONTROL"
        if os.path.isfile(portfile) == True:
            control_file = open(portfile)
            for line in control_file.readlines():
                if line == "\n" or line == "\r\n":
                    break
                findindex = line.find("Build-Depends:")
                if findindex != -1:
                    findindex +=len("Build-Depends:")
                    port_list=self.parse_portlist(line[findindex:len(line)])
                    break
            control_file.close()
        else:
            print("fail to open %s" % portfile)        
        return port_list

    def get_dependant_port(self,port):
        unique_port_list = []
        port_list =[port]
        for port in port_list:
            depend_list=self.read_port_from_control(port)
            if len(depend_list) != 0:
                port_list.extend(depend_list)     

        unique_port_list.extend(list(set(port_list)))
        return unique_port_list

    def remove_package_info(self,port_list,cur_triplet):
        status_file = self._vcpkg_root + os.sep+"installed"+ os.sep+"vcpkg"+os.sep+"status"
        content=""
        found_duplicate = False
        if os.path.isfile(status_file )==True:
            package_section=""
            lines = tuple(open(status_file, 'r'))
            for line in lines:
                if "\n" == line:
                    for cur_port in port_list:
                        port_find_index = package_section.find("Package: "+cur_port)
                        triplet_find_index = package_section.find("Architecture: "+cur_triplet)
                        if port_find_index != -1 and triplet_find_index != -1:
                            found_duplicate = True
                    if found_duplicate == False:
                        content += package_section
                        content += "\n"
                    package_section=""
                    found_duplicate = False
                else:
                    package_section += line

        return content

    def update_installed_vcpkg(self,repository,port_list,cur_triplet,conan_pkg_info):
        if len(conan_pkg_info) != 0:
            line_index=0
            linestrlist=[]
            content=""
            package_section=""
            status_file = self._vcpkg_root + os.sep+"installed"+ os.sep+"vcpkg"+os.sep+"status"
            for cur_port in port_list:
                if repository in conan_pkg_info.keys() and cur_triplet in conan_pkg_info[repository].keys() and cur_port in conan_pkg_info[repository][cur_triplet].keys():
                    package_section += "Package: "+cur_port+"\n"
                    package_section += "Architecture: "+cur_triplet+"\n"
                    for word in conan_pkg_info[repository][cur_triplet][cur_port]:
                        if word != "Dependant" and word != "Package_ID":
                            package_section += word+": "+str(conan_pkg_info[repository][cur_triplet][cur_port][word])+"\n"
                    package_section+="Status: install ok installed"+"\n"
                    package_section += "\n"
            if os.path.isfile(status_file )==True:
                content = self.remove_package_info(port_list,cur_triplet)
            content += package_section
            tools.save(status_file,content)

    def setdata_to_yml(self,filename,data):
        status=False
        with open(filename, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style = False)
        return status

    def get_installed_pkg_list(self):
        self.run("list > nul")
        installed_port = []
        status_file = self._vcpkg_root + os.sep+"installed"+ os.sep+"vcpkg"+os.sep+"status"
        if os.path.isfile(status_file )==True:
            lines = tuple(open(status_file, 'r'))
            installed_port = []
            port= ""
            triplet=""
            package_data={}
            for line in lines:
                if "Package:" in line:
                    port=line[0:len(line)-1].replace("Package: ","")
                elif "Architecture:" in line:
                    triplet=line[0:len(line)-1].replace("Architecture: ","")                    
                elif "Status:" in line:
                    if "Status: install ok installed" in line:
                        installed_port.append(port+":"+triplet)
        return installed_port

    def get_installed_pkg_data(self):
        self.run("list > nul")
        status_file = self._vcpkg_root + os.sep+"installed"+ os.sep+"vcpkg"+os.sep+"status"
        status = False
        installed_port = []
        tag_found=False
        if os.path.isfile(status_file )==True:
            status=True
            lines = tuple(open(status_file, 'r'))            
            port= ""
            triplet=""
            package_data={}
            installed_port_data={}
            for line in lines:
                if "Package" in line:
                    port=line[0:len(line)-1].replace("Package: ","")
                elif "Architecture" in line:
                    triplet=line[0:len(line)-1].replace("Architecture: ","")
                elif "Status:" in line:
                    if "Status: install ok installed" in line:     
                        installed_port.append(port+":"+triplet)
                        installed_port_data=self.update_package_info('local',port,triplet,package_data,installed_port_data)
                    package_data ={}
                elif line != "\n":                   
                    tokenlist=line.split(":")
                    if len(tokenlist[0]) < 15: 
                        value= ' '.join(tokenlist[1:])
                        data={tokenlist[0]:value[1:len(value)-1]}
                        package_data= {**package_data,**data}

        return installed_port,installed_port_data

    def update_package_info(self,repo,port,triplet,package_data,installed_port_data):
        if repo in installed_port_data.keys() and triplet in installed_port_data[repo].keys() and port in installed_port_data[repo][triplet].keys():
            installed_port_data[repo][triplet][port].update(package_data)
        elif repo in installed_port_data.keys() and triplet in installed_port_data[repo].keys():
            installed_port_data[repo][triplet].update({port:package_data})
        elif repo in installed_port_data.keys():
            installed_port_data[repo].update({triplet:{port:package_data}})
        else:
            installed_port_data[repo]= {triplet:{port:package_data}}
        return installed_port_data

def system(command):
    if os.path.isfile("vcpkgbin.log" )==False:
        command += " > vcpkgbin.log"
    else:
        command += " >> vcpkgbin.log"
    ret_code=os.system(command)
    return ret_code
