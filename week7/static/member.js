// 確認留言空值
let message = document.querySelector("input#message");
let leaveMessageBTN = document.querySelector("button#messageSubmit");
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
      PostDataByForm(messageID);
    }
  });
});

function PostDataByForm(data) {
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

// 會員姓名查詢
let queryBtn = document.querySelector("button#name_query");
queryBtn.addEventListener("click", (e) => {
  let query = document.querySelector("input#name_query").value;
  if (query) {
    url = "/api/member?username=" + query;
    fetch(url, {
      method: "GET",
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        if (data.data != null) {
          document.querySelector("p.name_query").innerHTML =
            data.data.name + " (" + data.data.username + ")";
        } else {
          document.querySelector("p.name_query").innerHTML =
            "查無此人 (No data)";
        }
      });
  } else {
    alert("請輸入帳號");
  }
});

// 更新姓名;
let renameBtn = document.querySelector("button#rename");
renameBtn.addEventListener("click", async (e) => {
  let newName = document.querySelector("input#rename").value;
  if (newName) {
    url = "/api/member";
    let data = {
      name: document.querySelector("input#rename").value,
    };
    response = await fetch(url, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    let result = await response.json();
    let resultTag = document.querySelector("p.rename_result");
    resultTag.innerHTML = result.ok ? "更新成功" : "更新失敗";
  } else {
    alert("請輸入名字");
  }
});
