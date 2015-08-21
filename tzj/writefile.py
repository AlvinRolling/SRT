#write_file

class WriteFile(object):
    
    def write_friend(self,uid,f_list):
        filename = "C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+".txt"
        print "filename: ", filename
        w = open(filename, "w")
        for item in f_list:
            w.write(item[0])
            w.write('\t')
            w.write(item[1])
            w.write('\n')
        w.close()
    
    def write_blog(self,uid,blog):
        filename = "C:/Users/hp1/Desktop/weibo_crawler/"+str(uid)+"_blog.txt"
        w =open(filename, "w")
        for item in blog:
            w.write(item)
            w.write('\n')
        w.close()
        
        