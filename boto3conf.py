info=[]
with open("/home/deno/.aws_creds") as f:
    for line in f:
        info.append(line.replace('\n',''))

