
// hsl is a method how uses variable h as a chromatic circle
function hslGenerator(numberColors){
    if(numberColors < 5){
        var circleRange = 70;
    }else if(numberColors < 9){
        var circleRange = 180;
    }else{
        var circleRange = 360;
    }
    var colors = [], c = 0, color = '', hRange = Math.floor(circleRange / numberColors), h = 0;
        while(c < numberColors){
            h = h + hRange <= circleRange ? h + hRange : circleRange;
            color = `hsl(${h}, 90%, 60%)`;
            colors.push(color);
            c++;
        }
    return colors;
}

function degrees2radius(degrees){
    return degrees * Math.PI / 180;
}

function negativeRow(myList){
    c = 0;
    for(let i = 1; i < myList.length; i++){
        if (myList[i] == -1){
            c++;
        }
    }
    return myList.length == c + 1 ? true : false;
}

function negative2zero(myList){
    for(let i = 1; i < myList.length; i++){
        myList[i] = myList[i] == -1 ? 0 : myList[i];
    }
    return myList;
}

function singleItemArray(myArray, deleteZero = false){
    let newArray = [];
    for(let i = 0; i < myArray.length; i++){
        if(!newArray.includes(myArray[i])){
            if(myArray[i] == 0 && deleteZero){
                continue
            }
            newArray.push(myArray[i]);
        }
    }
    return newArray;
}

function sumArray(array, start = 0){
    sum = 0;
    for(let i = start; i < array.length; i++){
        sum += array[i]
    }
    return sum;
}

function truncNumber(number, decimals) {
    b = number.toString().split(".");
    return b.length == 1 ? parseFloat(b[0]) : parseFloat(b[0] + '.' + b[1].slice(0, decimals));
}

function matrixConstructor(textFile){

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
    // Absolute mode
    }else{
        for(let i = 1; i < matrix.length; i++){
            for(let j = 1; j < matrix[i].length; j++){
                matrix[i][j] = parseInt(matrix[i][j]);
                if(!values.includes(matrix[i][j])){
                    values.push(matrix[i][j]);
                }
            }
        }
    }

    return [matrix, biggest, values];
}

function topValuesBySample(matrix, biggest){
    // Getting each matrix column without repeat one
    let column = [];
    var topValuesRange = document.getElementById('numberByTextInput').value
    let dictonaryTable = {}, biggestTable = 0;
    // Absolute Mode
    if (topValuesRange >= 1 || topValuesRange == 0){
        for(let i = 1; i < matrix[0].length; i++){
            for(let j = 1; j < matrix.length; j++){
                if(matrix[j][i] > biggestTable){
                    biggestTable = matrix[j][i];
                }
                // Creating dictionay with all items
                if (dictonaryTable[matrix[0][i]] === undefined){
                    dictonaryTable[matrix[0][i]] = {[matrix[j][0]] : matrix[j][i]};
                }else{
                    dictonaryTable[matrix[0][i]][matrix[j][0]] =  matrix[j][i];
                }
                if(!column.includes(matrix[j][i])){
                    column.push(matrix[j][i])
                }
            }
            column.sort(function(a, b) {return b - a;})
            var topValues = column.slice(0, topValuesRange);
            for(let j = 1; j < matrix.length; j++){
                // If this value is smaller than the range, it'll be -1
                if(matrix[j][i] < topValues[topValues.length - 1]){
                    matrix[j][i] = -1;
                }
            }
            column = [];
        }
        for(let i = matrix.length -1 ; i > 0; i--){
            if(negativeRow(matrix[i])){
                matrix.splice(i, 1);
            }else{
                matrix[i] = negative2zero(matrix[i]);
            }
        }
    // Relative Mode
    }else if(topValuesRange > 0){
        for(let i = 1; i < matrix[0].length; i++){
            columnSum = 0;
            for(let j = 1; j < matrix.length; j++){
                columnSum += matrix[j][i];
            }
            // EACH COLUMN
            // If this value is smaller than the range, it'll be -1
            for(let j = 1; j < matrix.length; j++){
                // Creating dictionay with all items
                if (dictonaryTable[matrix[0][i]] === undefined){
                    dictonaryTable[matrix[0][i]] = {[matrix[j][0]] : matrix[j][i]};
                }else{
                    dictonaryTable[matrix[0][i]][matrix[j][0]] =  matrix[j][i];
                }

                // Absolute Mode
                if (biggest > 1){
                    if(matrix[j][i] / columnSum < topValuesRange){
                        matrix[j][i] = -1;
                    }
                // Relative Mode
                }else{
                    if(matrix[j][i] < topValuesRange){
                        matrix[j][i] = -1;
                    }
                }
            }
            columnSum = 0;
        }
        for(let i = matrix.length -1 ; i > 0; i--){
            if(negativeRow(matrix[i])){
                matrix.splice(i, 1);
            }else{
                matrix[i] = negative2zero(matrix[i]);
            }
        }
    }else{
        alert('YOU CANNOT USE NEGATIVE VALUES!')
        throw new Error('YOU CANNOT USE NEGATIVE VALUES!');
    }
    return [matrix, dictonaryTable];
}

function reDictionaryTable(dictonaryTableCopy){
    var graphicValue = parseFloat(document.getElementById('numberByGraphicInput').value)

    if (graphicValue != 0){
        for (const [key, value] of Object.entries(dictonaryTableCopy)) {
            var sumValues = truncNumber(sumArray(Object.keys(value).map(function(k){return value[k];}), 0), 5);
            
            // All single items without zero
            var allTopItems = singleItemArray(Object.keys(value).map(function(k){return value[k];}), true).sort(function(a, b) {return b - a;}).slice(0, graphicValue)
            // Percent mode
            if (graphicValue < 1 && graphicValue > 0){
                for (const [k, v] of Object.entries(value)){
                    if(v != 0){
                        // If this animal is under cut range, it sums its value to "others" and delete original animal
                        if (v  / sumValues < graphicValue){
                            // Verify if there is a "others" key in dictionaryTable already
                            if (dictonaryTableCopy[key]['others'] === undefined){
                                dictonaryTableCopy[key]['others'] = v;
                            }else{
                                dictonaryTableCopy[key]['others'] +=  v;
                                dictonaryTableCopy[key]['others'] = truncNumber(dictonaryTableCopy[key]['others'], 5);
                            }
                            delete dictonaryTableCopy[key][k];
                        }
                        // Delete this animal if it is zero
                    }else{
                        delete dictonaryTableCopy[key][k];
                    }
                }
                // Absolute mode 
            }else{
                for (const [k, v] of Object.entries(value)){
                    if(v != 0){
                        // If this animal is under cut range (it's not one of the tops), it sums its value to "others" and delete original animal
                        if (!allTopItems.includes(v)){
                            // Verify if there is a "others" key in dictionaryTable already
                            if (dictonaryTableCopy[key]['others'] === undefined){
                                dictonaryTableCopy[key]['others'] = v;
                            }else{
                                dictonaryTableCopy[key]['others'] +=  v;
                                dictonaryTableCopy[key]['others'] = truncNumber(dictonaryTableCopy[key]['others'], 5);
                            }
                            delete dictonaryTableCopy[key][k];
                        }
                    }else{
                        delete dictonaryTableCopy[key][k];
                    }
                }
            }
        }
    }
        return dictonaryTableCopy;
}


function tableConstructor(matrix, values, biggest){
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
    // Separating values smaller or equal to average to left and bigger to right
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
    // Sort leftSide[] and rightSide[]
    leftSide.sort(function(a, b) {return a - b;});
    rightSide.sort(function(a, b) {return a - b;});
    // Buinding table rows
    for(let i = 1; i < matrix.length; i++){
        row += '<tr>';
        for(let j = 0; j < matrix[i].length; j++){
            if (j != 0){
                if(matrix[i][j] <= average){
                    rangeColor = parseFloat(1 / (leftSide.length));
                    index = leftSide.indexOf(matrix[i][j]);
                    rangeAlpha = parseFloat(1 - (rangeColor * index));
                    red = 0;
                    blue = 255;
                }else{
                    rangeColor = parseFloat(1 / (rightSide.length));
                    index = rightSide.indexOf(matrix[i][j]);
                    rangeAlpha = parseFloat((rangeColor * index) + rangeColor);
                    red = 255;
                    blue = 0;
                }
                dataBgColor = '(' + red + ', 0, ' + blue + ', ' + rangeAlpha + ')';
            }
            // We are using matrix[i][j]*1000/10 besides matrix[i][j]*100 because precision is better
            // Relative mode
            if (biggest <= 1 && biggest > 0){
                row += j == 0 ? '<td>' + matrix[i][j] + '</td>' : '<td style="background-color:rgba'+ dataBgColor + ';">' + matrix[i][j]*1000/10 + '%</td>';
            // Absolute mode
            }else{
                row += j == 0 ? '<td>' + matrix[i][j] + '</td>' : '<td style="background-color:rgba'+ dataBgColor + ';">' + matrix[i][j] + '</td>';
            }
        }
        row += '</tr>';
        table += row;
        row = '';
    }
    table += '</tbody></table>';
    return table;
}

function graphicConstructor(sample, reads, pizzaSection){
    function getCatetosDistance(thisPart){
        // Half angle of slice
        var specialInnerAngle = 360 * ((thisPart / 2) / 1000 * 10)
        // Value of inner angles from triangle formed by radius and Arch Base
        var sideInnerAngles = (180 - specialInnerAngle) / 2
        var degreesInRadius = degrees2radius(specialInnerAngle)
        //  a this, b anc c = radius
        // Distance from beggining until end of half arch formed 
        var archBasePerimeter = Math.sqrt( 2 * (radius * radius) - 2 * radius * radius * Math.cos(degreesInRadius))
        // Hypotenuse formeda by 
        var hypotenuse = (archBasePerimeter * Math.sin(degrees2radius(sideInnerAngles))) / Math.sin(degrees2radius(180 - (sideInnerAngles + sideInnerAngles - 45)));
        
        var currentDistance = (hypotenuse * Math.sin(degrees2radius(45))) / Math.sin(degrees2radius(90));

        return currentDistance;
    }

    // var circleLength = 2 * Math.PI * 50
    // var distanceMax = 150;
    // var testValues = [25, 15, 5, 8, 21, 16, 10].sort(function(a, b) {return b - a;});
    // var testValues = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10].sort(function(a, b) {return b - a;});
    // var testValues = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5].sort(function(a, b) {return b - a;});
    // var testValues = [33, 33, 17, 17].sort(function(a, b) {return b - a;});
    // var testValues = [50, 50].sort(function(a, b) {return b - a;});
    // var testValues = [33.33, 33.33, 33.33].sort(function(a, b) {return b - a;});
    // var testValues = [70, 28, 2].sort(function(a, b) {return b - a;});
    // var testValues = [25, 20, 55].sort(function(a, b) {return b - a;});
    // var testValues = [20, 20, 20, 20, 20].sort(function(a, b) {return b - a;});
    // var testValues = [100].sort(function(a, b) {return b - a;});

    // Delete animals with 0 in values
    for (const [animal, value] of Object.entries(reads)){
        if(value == 0){
            delete reads[animal]
        }
    }
    let keys = Object.keys(reads)
    var testValues = keys.map(function(k){return reads[k];})
    sum = sumArray(testValues, 0)
    
    pizzaSection.innerHTML += `<div class="pizzaContainer" id="${sample}-pizzaContainer">
                                    <div class="pizza" id="${sample}-pizza">
                                        <div class="pizzaBackground"></div>
                                    </div>
                                </div>`;
    let pizza = document.getElementById(`${sample}-pizza`);
    let pizzaContainer = document.getElementById(`${sample}-pizzaContainer`);
    let rotate = 0;
    let radius = 150;
    let last = 0;
    colors = hslGenerator(testValues.length);
    var label = `<div class="pizza-label-container">`;
    for(let i = 0; i < testValues.length; i++){
        
        part = testValues[i] * 100 / sum;
        let readValue = testValues[i] < 1 ? `${truncNumber(testValues[i] * 100, 2)}%` : testValues[i];
        label += `<div class="pizza-label">
                        <div class="label-color" style="background-color: ${colors[i]}">
                            ${readValue}
                        </div>
                        <div class="label-content">
                            <div class="animal-name">
                                ${keys[i]}
                            </div>
                            <div class="slice-percet">
                                ${truncNumber(part, 2)}%
                            </div>
                        </div>
                    </div>`

        pizza.innerHTML += `<div id="${sample}-pizzaSlice${i}" class="hold slice"><div class="pizza"></div></div>`;
        // How much the slice need to rotate to fit in the graphic
        // Current Percentegem 360º + Last Slice Percentegem 360º - Current Slice Percentegem 360º
        rotate += 360 * (part / 1000 * 10) + (last - 360 * (part / 1000 * 10))/2
        // Last Slice Percentegem 360º
        last = 360 * (part / 1000 * 10)
        if (part < 100){
            let firstPart = part - 50 > 0 ? 50 : part;
            let secondPart = part - 50 > 0 ? part - 50 : 0;
            if (firstPart <= 50){
                var currentDistance = getCatetosDistance(firstPart);
                var Lx = 50 - currentDistance, Ly = -100 + currentDistance, Rx = 50 + currentDistance, Ry = -100 + currentDistance;
                var slice = `polygon( ${Lx}% ${Ly}%, 50% 50%, ${Rx}% ${Ry}%, 50% -200%)`;
            }
            if(secondPart > 0){
                var currentDistance = getCatetosDistance(firstPart);
                Lx += currentDistance, Ly += currentDistance, Rx -= currentDistance, Ry += currentDistance;
                var slice = `polygon(-100% 0%, ${Lx}% ${Ly}%, 50% 50%, ${Rx}% ${Ry}%, 200% 0%)`;
            }
        
        }else{
            var slice = 'polygon(50% -100%, -100% 50%, 50% 200%, 200% 50%)'
        }

        var sliceElement = document.getElementById(`${sample}-pizzaSlice${i}`);
        sliceElement.style.clipPath = slice;
        sliceElement.style.transform = 'rotate('+ rotate +'deg)';
        sliceElement.style.backgroundColor = colors[i];
        sliceElement.style.position = 'absolute';
    }
    label += `</div>`;
    pizzaContainer.innerHTML += label;
}

function viewResult(){
    const divResults = document.getElementById('divResults');
    const viewModeRadios = document.getElementsByName('modeView');
    for(let i = 0; i < viewModeRadios.length; i++){
        if (viewModeRadios[i].checked == true){
            var viewMode = viewModeRadios[i].value;
            break;
        }
    }

    let file = document.getElementById("file");
    if(file.files.length > 0){
        let fr = new FileReader();
        fr.readAsText(file.files[0]);
        
        // If we use onloadend, we need to check the readyState.
        fr.onload = function() {
            let textFile = fr.result.split("\n");
            
            var [matrix, biggest, values] = matrixConstructor(textFile);
            var dictonaryTable = {};
            // Sorting values[]
            values.sort(function(a, b) {return a - b;});
            // Building Matrix
            [matrix, dictonaryTable] = topValuesBySample(matrix, biggest);
            // {...dictonaryTable} makes a copy of dictonaryTable
            dictonaryTable = reDictionaryTable({...dictonaryTable});
            divResults.innerHTML = '';
            if([1, 3].includes(parseInt(viewMode))){
                // Building Table
                table = tableConstructor(matrix, values, biggest);
                divResults.innerHTML = table;
            }
            if([2, 3].includes(parseInt(viewMode))){
                divResults.innerHTML += `<div class="pizza-section" id="pizza-section"></div>`;
                const pizzaSection = document.getElementById('pizza-section');
                for (const [sample, reads] of Object.entries(dictonaryTable)){
                    // Building and pizza graphic to html document
                    graphicConstructor(sample, reads, pizzaSection);
                }
            }
        }
    }else{
        alert('YOU SHOULD INFORM A MATRIX AS A TXT FILE!')
    }

}
