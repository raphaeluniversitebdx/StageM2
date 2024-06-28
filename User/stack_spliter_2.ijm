dir1=getDirectory("Choose source directory");
list=getFileList(dir1);
filenames=newArray(list.length/2);
createdir=dir1+"Split_folder"+File.separator;
File.makeDirectory(createdir);
tt=0;

for (i=0; i<list.length; i++) {
	h=endsWith(list[i],"tiff");
	if (h==1) {
		filenames[tt]=list[i];
		setBatchMode(true);
		open(dir1+filenames[tt]);
		frames=nSlices;
		run("Stack to Images");

		subdir=createdir+filenames[tt]+File.separator;
		File.makeDirectory(subdir);
    
		for (k=0; k<frames; k++) {
			saveAs("Tiff",subdir+getTitle);
			close();
			}
		tt=tt+1;
	}		
}