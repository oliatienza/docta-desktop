function saveBinaryImage(img, path, format){
    run("Make Binary");
    saveAs(format, path);
}

function saveSkeletonImage(img, path){
    run("Skeletonize");
    saveAs(format, path);
}

original = getDirectory("Select source folder");
bOutput = getDirectory("Select output path for binary images");
sOutput = getDirectory("Select output path for skeleton images");

list = getFileList(original)
for(i = 0; i < list.length; i++){
    open(original + list[i]);
    run("Make Binary");
    saveAs("BMP", bOutput + list[i]);
    run("Skeletonize");
    saveAs("BMP", sOutput + list[i]);
    close();
}