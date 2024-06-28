// MIP for segmentation with Imjoy


// Pour aue le script fonctionne il faut 
// creer un sous dossier MIP qui devra contenir les projections 
var in = "";

in=getDirectory("Choose a Directory");
print(in);
run("Close All");
setBatchMode(true);
openAndMax();

function openAndMax(){
	files=getFileList(in);

	for(i=0; i<files.length; i++){
		if(endsWith(files[i], ".tiff")){
		open(in+files[i]);
		getDimensions(width, height, channels, slices, frames);
		if(slices > 1){
		run("Z Project...", "projection=[Max Intensity]");
		saveAs("Tiff", in+"MIP/MAX_"+files[i]);
		run ("Close All");
		}
		else{
			saveAs("Tiff", in+"MIP/MAX_"+files[i]); // rajoute MAX_ en debut des fichiers de projections 
			run ("Close All");
		}
		}
	}
}
