// var optionsUrl="{{ url_for('static', filename='config/web_options.json') }}" 
var optionsUrl="static/config/web_options.json" 
var modelSelect = document.getElementById("model-select");
var confirmButton = document.getElementById("confirm-button");
var currentModel = document.getElementById("current-model");
var listGroup = document.getElementById('list-group');
var prompt_seletor = document.getElementById('prompt');
// 初始化prompt模版文件路径
fetch('/prompt-file')
  .then(response => response.json())
  .then(data => {
    // 根据 JSON 中的值设置下拉框的选项
    data.forEach(item => {
      var optionElement = document.createElement("option");
      optionElement.value = item;
      optionElement.text = item;
      prompt_seletor.appendChild(optionElement);
    });
  })
  .catch(error => {
    console.log("加载下拉选项内容时发生错误:", error);
  });

  // 发送 AJAX 请求，读取包含下拉框选项的 JSON 文件
fetch(optionsUrl)
  .then(response => response.json())
  .then(data => {
    var dropdown = document.getElementById("model-select");

    // 根据 JSON 中的值设置下拉框的选项
    Object.keys(data).forEach(key => {
      var optionElement = document.createElement("option");
      optionElement.value = key;
      optionElement.text = key;
      dropdown.appendChild(optionElement);
    });
  })
  .catch(error => {
    console.log("加载下拉选项内容时发生错误:", error);
  });

function updataSecondSelectOptions(){
  var selectElement_model = document.getElementById("model-select").value;
  var secondSelect = document.getElementById("conversation_method");
  // 发送 AJAX 请求，读取包含选项值的 JSON 文件
  $.getJSON(optionsUrl, function(data) {
    // 根据选中的值更新第二个下拉框的选项
    console.log(data, selectElement_model)
    var options = data[selectElement_model];
    var html = "";
    for (var i = 0; i < options.length; i++) {
      html += "<option value='" + options[i] + "'>" + options[i] + "</option>";
    }
    secondSelect.innerHTML = html;
  });
}

function updataPrompt(){
  var prompt_value = prompt_seletor.value;
  fetch('/prompt-selected', {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ 'prompt_value': prompt_value })
    })
    .then(response => response.json())
    .catch(error => {
      console.log("加载下拉选项内容时发生错误:", error);
    });
}

// 确认按钮点击事件处理函数
function handleConfirm(){
    selectedModel = modelSelect.value
    if (selectedModel !== "" && selectedModel !== currentModel.value) {
      confirmButton.disabled = true
      currentModel.value = '加载中...';
      sendModelSelection(selectedModel);
    }
};

// 向后台发送模型选择信号的函数
function sendModelSelection(model) {
  fetch("/model-selection", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ 'model_type': model })
  })
  .then(response => {
      console.log(response.ok)
      if (response.ok) {
          console.log(response.ok);
          console.log("模型选择成功");
          currentModel.value = selectedModel;
          // 清空list-group中的内容
          listGroup.innerHTML = '';
          // 清除sessionId中的历史存储信息
          const sessionId = Date.now().toString();
          sessionStorage.removeItem(sessionId);
        } else {
          console.error("模型选择失败");
          currentModel.value = '';
      }
      confirmButton.disabled = false
  })
    .catch(error => {
      console.error("请求错误:", error);
  });
}
