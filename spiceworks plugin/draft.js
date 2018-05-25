'use strict';
var a = 123
console.log(a)

var fn = x => x*x;
console.log(fn(2));

a = typeof alert;
console.log(a); //function

function Student (name) {
    this.name = name;
}

var jiajun = new Student('Jia Jun');
console.log(Object.getPrototypeOf(jiajun));
