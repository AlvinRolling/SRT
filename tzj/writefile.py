#write_file
class WriteFile(object):
    
    def write_fans(self,uid,result): 
        l = len(result)
        #w = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_fans.txt","w")
        #id_only = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_fans_id.txt","w")
        w = open(str(uid)+"/"+str(uid)+"_fans.txt","w")
        id_only = open(str(uid)+"/"+str(uid)+"_fans_id.txt","w")
        for i in range(0,l):
            if(len(result[i]) > 0):
                m = len(result[i])
                for j in range(0,m):
                    if(int(result[i][j]['follow'])>1000 or int(result[i][j]['fans'])>1000):
                        print "Omit user: ",int(result[i][j]['id'])
                        #print "follow: ",int(result[i][j]['follow'])
                        #print "fans: ",int(result[i][j]['fans'])
                        
                        #ow = open("C:/Users/hp1/Desktop/weibo_crawler/omitted_user.txt","a+")
                        ow = open("omitted_user.txt","a+")
                        ow.write(str(result[i][j]['id']))
                        ow.write('\t')
                        ow.write(str(result[i][j]['follow']))
                        ow.write('\t')
                        ow.write(str(result[i][j]['fans']))
                        ow.write('\n')
                        ow.close()
                        continue
                    # don't need these nodes, it's not a single person 
                    key = result[i][j].keys()
                    for item in key:
                        w.write(item)
                        w.write(": \t")
                        w.write(str(result[i][j][item]))
                        w.write('\n')
                    w.write('\n')
                    id_only.write(str(result[i][j]['id']))
                    id_only.write('\t')
                    id_only.write(str(result[i][j]['follow']))
                    id_only.write('\t')
                    id_only.write(str(result[i][j]['fans']))
                    id_only.write('\n')
                    # there a special text file to record the basic info of users(id,follow_num,fans_num)
        w.close()
        id_only.close()
    
    def write_blog(self,uid,scratch_result):
        #filename = "C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_blog.txt"
        filename = str(uid)+"/"+str(uid)+"_blog.txt"
        w = open(filename,"w")
        L = len(scratch_result)
        for i in range(0,L):
            key = scratch_result[i].keys()
            for item in key:
                w.write(item)
                
                if(item == 'nc' or item == 'lp' or item == 'repost'):
                    w.write(": ")
                    for at in scratch_result[i][item]:
                        w.write("\t")
                        w.write(str(at))
                elif(item == 'comment'):
                    w.write(": ")
                    for com in scratch_result[i][item]:  # write each comment
                        w.write(com[0][0])
                        w.write("\t")
                        w.write(com[0][1])
                        w.write("\t")
                        w.write(com[1])
                        w.write("\t")
                        w.write(com[2])
                        w.write("\t")
                        w.write("//")
                else:
                    w.write(": \t")
                    w.write(str(scratch_result[i][item]))
                w.write('\n')
            w.write('\n')
        w.close()

    def write_follows(self,uid,result):
        l = len(result)
        #w = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_follows.txt","w")
        #id_only = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_follows_id.txt","w")
        w = open(str(uid)+"/"+str(uid)+"_follows.txt","w")
        id_only = open(str(uid)+"/"+str(uid)+"_follows_id.txt","w")
        for i in range(0,l):
            if(len(result[i]) > 0):
                m = len(result[i])
                for j in range(0,m):
                    if(int(result[i][j]['follow'])>1000 or int(result[i][j]['fans'])>1000):
                        print "Omit user: ",int(result[i][j]['id'])
                        #print "follow: ",int(result[i][j]['follow'])
                        #print "fans: ",int(result[i][j]['fans'])
                        #ow = open("C:/Users/hp1/Desktop/weibo_crawler/omitted_user.txt","a+")
                        ow = open("omitted_user.txt","a+")
                        ow.write(str(result[i][j]['id']))
                        ow.write('\t')
                        ow.write(str(result[i][j]['follow']))
                        ow.write('\t')
                        ow.write(str(result[i][j]['fans']))
                        ow.write('\n')
                        ow.close()
                        continue
                    # don't need these nodes, it's not a single person 
                    key = result[i][j].keys()
                    for item in key:
                        w.write(item)
                        w.write(": \t")
                        w.write(str(result[i][j][item]))
                        w.write('\n')
                    w.write('\n')
                    id_only.write(str(result[i][j]['id']))
                    id_only.write('\t')
                    id_only.write(str(result[i][j]['follow']))
                    id_only.write('\t')
                    id_only.write(str(result[i][j]['fans']))
                    id_only.write('\n')
                    # there a special text file to record the basic info of users(id,follow_num,fans_num)
        w.close()
        id_only.close()
        