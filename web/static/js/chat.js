let isProcessing = false;
const sessionId = Date.now().toString();
const chatHistoryStr = sessionStorage.getItem(sessionId);
var chatHistory = chatHistoryStr ? JSON.parse(chatHistoryStr):[['你是谁？','我是人工智能Hai。']];
let link_text_id = 0;

function isInputValid(){
    const input = document.getElementById("chat-input").value.trim();
    return input !== "";
}
function handleKeyDown(event){
    if (event.keyCode == 13 && isInputValid()) {
        if (!isProcessing){
        handleClick();
        }
    }
}
function handleClick(){
    var currentModel = document.getElementById("current-model").value;
    if (!isInputValid() || currentModel==""){
        return 
    }
    if (!isProcessing){
        isProcessing = true;
    }
    var selectElement_conversation = document.getElementById("conversation_method").value;
    var button = $("#gpt-button");
    var loading = $('#loading');
    var question = $("#chat-input").val();

    // 显示加载指示器并禁用按钮
    $("#loading").removeClass("d-none");
    $("#gpt-button").prop("disabled", true);
    const options = {
        mangle: false,
        headerIds: false
        };
    // 使用 options 进行 marked.js 的初始化
    marked.setOptions(options);
    var html_question = marked.parse(question);
    var img = $("<img>", {
            src:"static/images/duck.jpg",
            alt:"twbs",
            width:"32",
            height:"32",
            class:"rounded-circle flex-shrink-0",
        })

    // 创建一个新的链接元素
    var link = $("<li>", {
        href: "#",
        class: "list-group-item list-group-item-action d-flex gap-3 py-3",
        html: html_question
        }).prepend(img);

    // 将链接元素添加到列表中
    $("#list-group").append(link);
    $("#chat-input").val('');

    fetch('/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'model':currentModel,'conversation':selectElement_conversation,'prompt': question,'history': JSON.stringify(chatHistory)})
        })
        .then(response => {
            // var html = marked.parse(response.answer);
            var img = $("<img>", {
            src: "static/images/favicon.png",
            alt: "twbs",
            width: "32",
            height: "32",
            class: "rounded-circle flex-shrink-0 margin-pos"
            });
            var link = $("<li>", {
            href: "#",
            class: "list-group-item list-group-item-action flex-column gap-3 py-3",
            html: img.add($("<span>").css("height","5rem").attr("id","link-text-"+link_text_id))
            });
            $("#list-group").append(link);
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let lastIndex = 0;
            let markdownData = '';
            // readChunk实现持续通信
            const readChunk = () => {
                reader.read().then(({ done, value }) => {
                    const data = decoder.decode(value);
                    const newData = data.slice(lastIndex);
                    console.log(newData, lastIndex);
                    const linkText = $("#link-text-"+link_text_id);
                    markdownData += newData
                    htmldata = marked.parse(markdownData);

                    linkText.html(htmldata)
                    lastIndex = data.length; // 更新最后的索引位置
                    // 通信完成标志
                    if (done) {
                        // 隐藏加载指示器并解锁按钮
                        $("#loading").addClass("d-none");
                        $("#gpt-button").prop("disabled", false);
                        console.log(link_text_id);
                        link_text_id++;

                        const newHistroyTuple = [question, markdownData];
                        chatHistory.push(newHistroyTuple);
                        sessionStorage.setItem(sessionId, JSON.stringify(chatHistory));
                        isProcessing = false
                        return;
                    }
                    readChunk();
                });
            };
            readChunk();
            })
        .catch(error => {
            // 处理错误
            });
};