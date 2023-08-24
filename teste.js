/*function counter() {
    let n = 0;
    return {
        count: function () { return n++; },
        reset: function () { n = 0; }
    };
}
// Cada invocação de counter() cria um novo escopo independente dos escopos que podem ser usados por outras invocações!
let c = counter(), d = counter();
c.count()
d.count()

c.reset();
c.count();
d.count();
*/
/*
function counter(n) {
    return {
        get count() { return n++; },
        set count(m) {
            if (m > n) n = m;
            else throw Error("count can only be set to a larger value");
        }
    };
}

let k = counter(1000);
console.log(k.count);
console.log(k.count);
counter.count = 2000;
*/

function addPrivateProperty(o, name, predicate) {
    let value;

    o[`get${name}`] = function () { return value; };
}


console.log('Teste');