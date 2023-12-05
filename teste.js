const readline = require("readline").createInterface({
  input: process.stdin,
  output: process.stdout,
});

readline.question("Type a number \n", (number) => {
  console.log(
    `The ${number}th number of Fibonacci sequence is: ${fib(number)}!`
  );
  readline.close();
});

const fib = (n) => {
  if (n <= 2) return 1;
  return fib(n - 1) + fib(n - 2);
};
