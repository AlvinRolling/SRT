#write_file

class WriteFile(object):
    
    def write_friend(self,uid,result): 
        l = len(result)
        w = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_friends.txt","w")
        id_only = open("C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_friends_id.txt","w")
        for i in range(0,l):
            if(len(result[i]) > 0):
                m = len(result[i])
                for j in range(0,m):
                    key = result[i][j].keys()
                    for item in key:
                        w.write(item)
                        w.write(": \t")
                        w.write(str(result[i][j][item]))
                        w.write('\n')
                    w.write('\n')
                    id_only.write(str(result[i][j]['id']))
                    id_only.write('\n')
        w.close()
        id_only.close()
    
    def write_blog(self,uid,scrach_result):
        filename = "C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_blog.txt"
        w = open(filename,"w")
        L = len(scrach_result)
        for i in range(0,L):
            key = scrach_result[i].keys()
            for item in key:
                w.write(item)
                w.write(": \t")
                w.write(str(scrach_result[i][item]))
                w.write('\n')
            w.write('\n')
        w.close()
        