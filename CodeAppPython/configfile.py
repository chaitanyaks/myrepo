import yaml

def yaml_loader(filepath):
    with open(filepath,"r")as file_descriptor:
        data=yaml.load(file_descriptor)
        print data

def yaml_dump(filepath1,data):
    with open(filepath,"w") as file_descriptor:
        test=yaml.dump(data, file_descriptor)
        print test
    return test


if __name__=="__main__":
    filepath="testconfig.yaml"
    filepath1="testconfig1.yaml"
    data= yaml_loader(filepath)
    print data
    test=yaml.dump(filepath1,data)
    print test

    #check=yaml_dump(filepath1,data)
    #print check
    

##    items = data.get('items')
##    print items
##    for item_name,item_value in items.iteritems():
##        print item_name,item_value

#yaml_loader(r"F:/Boto3/CodeAppPython/test1.yaml")



##x=yaml.dump(data)
##print x
