// 確認sigin in 是否有空值
let userName = document.querySelector("input#username");

let signinBTN = document.querySelector("button#signinSubmit");
signinBTN.addEventListener("click", (e) => {
  if (userName.value == "") {
    alert("Please input your username and password");
    e.preventDefault();
  }
});
