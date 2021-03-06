# Copyright 2009-2014 Eucalyptus Systems, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#
# Please contact Eucalyptus Systems, Inc., 6755 Hollister Ave., Goleta
# CA 93117, USA or visit http://www.eucalyptus.com/licenses/ if you need
# additional information or have any questions.
import subprocess
import commands
import os
import json
import servo
import servo.config as config

class FloppyCredential(object):
    def __init__(self):
        #check if floppy is mounted. if not mount it
        try:
            if not self.is_floppy_mounted():
                self.mount_floppy()
            f = None
            f = open('%s/credential' % config.FLOPPY_MOUNT_DIR)
            cred = None
            if f:
                cred = credential =json.load(f)
                f.close()
            self.unmount_floppy()
            self.iam_pub_key = cred['iam_pub_key']
            self.iam_pub_key = self.iam_pub_key.strip().decode('base64')
            self.instance_pub_key = cred['instance_pub_key']
            self.instance_pub_key = self.instance_pub_key.strip().decode('base64')
            self.instance_pk = cred['instance_pk']
            self.instance_pk = self.instance_pk.strip().decode('base64')
            self.iam_token = cred['iam_token']  
            self.iam_token = self.iam_token.strip()  
        except IOError, err:
            servo.log.error('failed to read credential file on floppy: '+str(err)) 
            raise Exception()
        except Exception, err:
            servo.log.error('failed to parse credential file: '+str(err))
            raise Exception()

    @staticmethod
    def is_floppy_mounted(dev_str='/dev/fd0'):
        cmd_line = 'sudo mount | grep %s > /dev/null' % dev_str
        if subprocess.call(cmd_line, shell=True) == 0:
            return True
        else:
            return False

    @staticmethod
    def mount_floppy(dev='/dev/fd0', dir=config.FLOPPY_MOUNT_DIR):
        if not os.path.exists(dir):
            os.makedirs(dir)
        cmd_line = 'sudo mount %s %s' % (dev,dir)
        if subprocess.call(cmd_line, shell=True) == 0:
            servo.log.debug('floppy disk mounted on '+dir) 
        else:
            raise Exception('failed to mount floppy')

    @staticmethod
    def unmount_floppy(dir=config.FLOPPY_MOUNT_DIR):
        if not os.path.exists(dir):
            return
        cmd_line = 'sudo umount %s' % dir
        if subprocess.call(cmd_line, shell=True) == 0:
            servo.log.debug('floppy disk unmounted on '+dir) 
        else:
            raise Exception('failed to unmount floppy')
    
    def get_iam_pub_key(self):
        return self.iam_pub_key

    def get_instance_pub_key(self):
        return self.instance_pub_key

    def get_instance_pk(self):
        return self.instance_pk

    def get_iam_token(self):
        return self.iam_token 
