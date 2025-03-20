var year;
function isLeap (year) {
    print("Digite o ano");
    prompt(year);
    if(year % 4 == 0 && !(year % 100 == 0) || year % 400 == 0) {
        return "is leap";
    } else {
        return "is not leap"
    }
}

console.log(isLeap());