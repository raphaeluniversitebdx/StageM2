dir1=getDirectory("Choose source directory");
list=getFileList(dir1);
filenames=newArray(list.length/2);
createdir=dir1+"Hyperstack_splitter_folder"+File.separator;
File.makeDirectory(createdir);

// Recuperation des dimensions du stack
Stack.getDimensions(width, height, channels, slices, frames); 

print("slices" + slices + "frames" + frames); 

// photobleaching correction sur l'hyperstack 
// run("Bleach Correction", "correction=[Exponential Fit]");

// Utilisation de stack splitter 
run("Stack Splitter", "number=" + frames);

// Sauvegarde des images ouvertes 
findImg("stk")

//-------------------------------------------------------------------------------------------------------
function findImg(arg){ // arg = mot clé à chercher ; name = nom pour renommage
	imgTitles=getList("image.titles");
	//Array.print(imgTitles);
	for (i = 0; i < imgTitles.length; i++) {
		if(matches(imgTitles[i], ".*"+arg+".*")){
			selectImage(imgTitles[i]);
			
			// ICI rentre le code que tu veux appliquer à l'image trouvée.
			saveAs("Tiff", createdir+imgTitles[i]);
			close(imgTitles[i]);
			
		}
	}
	run("Tile");
}
