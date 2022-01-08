function viewResult(){
    let file = document.getElementById("file");
    let fr = new FileReader();

    fr.readAsText(file.files[0]);

    // If we use onloadend, we need to check the readyState.
    fr.onload = function() {
        let textFile = fr.result.split("\n");
        let matrix = [];
        for(let i = 0; i < textFile.length; i++){
            let row = textFile[i].replace(/(\r\n|\n|\r)/gm, "").split("\t");
            if (row.length > 1){
                matrix.push(row);
            }
            row = [];
        }
        console.log(matrix);
    }

}