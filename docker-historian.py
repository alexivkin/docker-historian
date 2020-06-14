#!/usr/bin/env python3

# Reverse engineering Dockerfile from docker history
# Pretty prints docker history

import os,sys

from docker import Client

class ImageNotFound(Exception):
    def __init__(self,e):
        print(e)
        sys.exit(1)

class MainObj(object):
    def __init__(self):
        super(MainObj, self).__init__()
        self.cmds = []
        base_url='unix://var/run/docker.sock' # could be blank for linux
        if os.getenv('DOCKER_HOST'):
            base_url=os.getenv('DOCKER_HOST')+":2375"
        self.cli = Client(base_url)
        self.get_image(sys.argv[-1])
        self.hist = self.cli.history(self.img['RepoTags'][0])
        self.parse_history()
        self.cmds.reverse()
        self.print_cmds()

    def print_cmds(self):
        for i in self.cmds:
            print(i)

    def get_image(self, img_hash):
        imgs = self.cli.images()
        #print(imgs)
        for i in imgs:
            #print(i,i['RepoTags'])
            if img_hash in i['Id'] or (i['RepoTags'] is not None and any(t.startswith(img_hash) for t in i['RepoTags'])):
                self.img = i
                return
        raise ImageNotFound("Image {} not found\n".format(img_hash))

    def insert_step(self, step):
        if "#(nop)" in step:
            to_add = step.split("#(nop) ")[1]
        elif step.startswith("/bin/sh -c "):
            to_add = "RUN "+step.replace("/bin/sh -c ","")
        else:
            to_add = ("RUN {}".format(step))
        to_add = to_add.replace("&&", "\\\n    &&")
        self.cmds.append(to_add.strip(' '))

    def parse_history(self):
        first_tag = False
        actual_tag = False
        for i in self.hist:
            if i['Tags']:
                actual_tag = i['Tags'][0]
                if first_tag:
                    first_tag = False
                    break
                first_tag = True
            self.insert_step(i['CreatedBy'])
        if first_tag:
            self.cmds.append("FROM scratch")
        else:
            self.cmds.append("FROM {}".format(actual_tag))

if len(sys.argv) < 2:
    print("Need an image name or a part thereof")
else:
    my_obj = MainObj()
