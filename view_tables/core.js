
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
    if (topValuesRange >= 1 || topValuesRange == 0){
        for(let i = 1; i < matrix[0].length; i++){
            for(let j = 1; j < matrix.length; j++){
                if(!column.includes(matrix[j][i])){
                    column.push(matrix[j][i])
                }
            }
            column.sort(function(a, b) {return b - a;})
            var topValues = column.slice(0, topValuesRange);
            for(let j = 1; j < matrix.length; j++){
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
    }else if(topValuesRange > 0){
        for(let i = 1; i < matrix[0].length; i++){
            columnSum = 0;
            for(let j = 1; j < matrix.length; j++){
                columnSum += matrix[j][i];
            }

            for(let j = 1; j < matrix.length; j++){
                if (biggest > 1){
                    if(matrix[j][i] / columnSum < topValuesRange){
                        matrix[j][i] = -1;
                    }
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

    return matrix;
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

function graphicConstructor(){
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

    var graphicValue = document.getElementById('numberByGraphicInput').value
    var circleLength = 2 * Math.PI * 50
    var distanceMax = 150;
    // var testValues = [25, 15, 5, 8, 21, 16, 10].sort(function(a, b) {return b - a;});
    // var testValues = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10].sort(function(a, b) {return b - a;});
    // var testValues = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5].sort(function(a, b) {return b - a;});
    // var testValues = [33, 33, 17, 17].sort(function(a, b) {return b - a;});
    // var testValues = [50, 50].sort(function(a, b) {return b - a;});
    // var testValues = [33.33, 33.33, 33.33].sort(function(a, b) {return b - a;});
    // var testValues = [70, 28, 2].sort(function(a, b) {return b - a;});
    var testValues = [25, 20, 55].sort(function(a, b) {return b - a;});
    // var testValues = [20, 20, 20, 20, 20].sort(function(a, b) {return b - a;});
    // var testValues = [100].sort(function(a, b) {return b - a;});
    
    divResults.innerHTML += '<div class="pizzaContainer" id="pizzaContainer"><div class="pizzaBackground"></div></div>';
    let pizzaContainer = document.getElementById('pizzaContainer');
    let rotate = 0;
    let radius = 150;
    let last = 0;
    colors = hslGenerator(testValues.length);
    for(let i = 0; i < testValues.length; i++){
        part = testValues[i];
        pizzaContainer.innerHTML += '<div id="pizzaSlice'+ i +'" class="hold slice"><div class="pizza"></div></div>';
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
        var sliceElement = document.getElementById(`pizzaSlice${i}`);
        sliceElement.style.clipPath = slice;
        sliceElement.style.transform = 'rotate('+ rotate +'deg)';
        sliceElement.style.backgroundColor = colors[i];
        sliceElement.style.position = 'absolute';
        
    }
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
            
            // Sorting values[]
            values.sort(function(a, b) {return a - b;});
            // Building Matrix
            matrix = topValuesBySample(matrix, biggest);
            divResults.innerHTML = '';
            if([1, 3].includes(parseInt(viewMode))){
                // Building Table
                table = tableConstructor(matrix, values, biggest);
                divResults.innerHTML = table;
            }
            if([2, 3].includes(parseInt(viewMode))){
                graphicConstructor();
            }
        }
    }else{
        alert('YOU SHOULD INFORM A MATRIX AS A TXT FILE!')
    }

}
