function sumArray(array){
    sum = 0;
    for(let i = 1; i < array.length; i++){
        sum += array[i]
    }
    return sum;
}

function truncNumber(number, decimals) {
    b = number.toString().split(".");
    return b.length == 1 ? parseFloat(b[0]) : parseFloat(b[0] + '.' + b[1].slice(0, decimals));
}

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
        let biggest = 0;
        for(let i = 1; i < matrix.length; i++){
            for(let j = i; j < matrix[i].length; j++){
                if(parseFloat(matrix[i][j]) > biggest){
                    biggest = parseFloat(matrix[i][j]);
                }
            }
        }
        let values = [];
        // Relative mode
        if (biggest <= 1 && biggest > 0){
            for(let i = 1; i < matrix.length; i++){
                for(let j = 1; j < matrix[i].length; j++){
                    matrix[i][j] = truncNumber(matrix[i][j], 2);
                    if(!values.includes(matrix[i][j])){
                        values.push(matrix[i][j]);
                    }
                }
            }
        }
        // Absolute mode
        values.sort();  
        console.log(matrix);
        console.log(values);
        // Building table
        average = values.length > 1 ? (values[values.length - 1] + values[0]) / 2 : values[0];
        table = '<table class="tableResult">';
        header = '<thead><tr>'
        row = '';
        for(let i = 0; i < matrix[0].length; i++){
            header += '<td>' + matrix[0][i] + '</td>';
        }
        header += '</tr></thead>';
        table += header;
        table += '<tbody>';
        leftSide = []
        rightSide = []
        for(let i = 1; i < matrix.length; i++){
            for(let j = 1; j < matrix[i].length; j++){
                if (parseFloat(matrix[i][j]) <= average){
                    if(!leftSide.includes(matrix[i][j])){
                        leftSide.push(matrix[i][j]);
                    }
                }else{
                    if(!rightSide.includes(matrix[i][j])){
                        rightSide.push(matrix[i][j]);
                    }
                }
            }
        }
        leftSide.sort();
        rightSide.sort();
        console.log(leftSide);
        console.log(rightSide);
        for(let i = 1; i < matrix.length; i++){
            row += '<tr>';
            for(let j = 0; j < matrix[i].length; j++){
                if (j != 0){
                    if(matrix[i][j] <= average){
                        rangeColor = parseFloat(1 / (leftSide.length));
                        index = leftSide.indexOf(matrix[i][j]);
                        rangeAlpha = parseFloat(1 - (rangeColor * index));
                        console.log('Left:' + rangeAlpha);
                        red = 0;
                        blue = 255;
                    }else{
                        rangeColor = parseFloat(1 / (rightSide.length));
                        index = rightSide.indexOf(matrix[i][j]);
                        rangeAlpha = parseFloat((rangeColor * index) + rangeColor);
                        console.log('Right:' + rangeAlpha);
                        red = 255;
                        blue = 0;
                    }
                    dataBgColor = '(' + red + ', 0, ' + blue + ', ' + rangeAlpha + ')';
                }
                // We are using matrix[i][j]*1000/10 besides matrix[i][j]*100 because precision is better
                row += j == 0 ? '<td>' + matrix[i][j] + '</td>' : '<td style="background-color:rgba'+ dataBgColor + ';">' + matrix[i][j]*1000/10 + '%</td>';
            }
            row += '</tr>';
            table += row;
            row = '';
        }
        table += '</tbody></table>';
        let divResults = document.getElementById('divResults');
        divResults.innerHTML = table;
        console.log(average);
        console.log(table);
    }

}