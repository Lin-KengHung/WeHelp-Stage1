// 確認留言空值
let message = document.querySelector("input#message");
let leaveMessageBTN = document.querySelector("button#messageSubmit");
console.log(leaveMessageBTN);
leaveMessageBTN.addEventListener("click", (e) => {
  if (message.value == "") {
    alert("Say something, I'm giving up on you");
    e.preventDefault();
  }
});
// 刪除留言
let deleteBtns = document.querySelectorAll("button.trash");
deleteBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    let messageID = btn.parentElement.id;
    let answer = confirm("Are you sure about that???");
    if (answer === true) {
      PostDataByForm(btn, messageID);
    }
  });
});

function PostDataByForm(btn, data) {
  let form = document.createElement("form");
  form.method = "POST";
  form.action = "/deleteMessage";
  let input = document.createElement("input");
  input.type = "hidden";
  input.name = "data";
  input.value = data;
  form.appendChild(input);
  document.body.appendChild(form);
  form.submit();
}
