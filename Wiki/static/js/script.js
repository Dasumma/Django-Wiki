const delay = ms => new Promise(res => setTimeout(res, ms));


function start(){
    tableToggle();
    setHTML();
}
function startHome(){
    showMenu();
    homeButton();
}

const tableToggle = () => {
    if(document.getElementById("show_table") == null) return;
    let btn_main_search = document.getElementById("show_table");
        
    btn_main_search.addEventListener("click", function() {
        let info_table = document.getElementById("info_table");
        info_table.hidden = !info_table.hidden;
        
        if(info_table.hidden == false || info_table.hidden == null)
            btn_main_search.innerText="Hide Details";
        else
            btn_main_search.innerText="Details";
    });    

    document.onload = null;
}

const setHTML = (content) => {

    if(document.getElementById("MainContent") == null) return;
    let main_content_area = document.getElementById("MainContent");
    let content_to_parse = main_content_area.innerText;

    const parser = new DOMParser();
    const html = parser.parseFromString(content_to_parse, 'text/html');
    const body = document.createElement("p");
    body.innerHTML = html.body.innerHTML;

    main_content_area.innerText = "";
    main_content_area.appendChild(body);
    if(document.getElementsByTagName("table") == null) return;
    [...(document.getElementsByTagName("table"))].forEach((a) => {
        a.className = "";
        a.classList.add("table");
    })
}

const fixTextAreas = () =>{
    document.getElementById("id_summary").style = "vertical-align:middle";
    document.getElementById("id_keywords").style = "vertical-align:middle";
    document.getElementById("id_userAccess").style = "vertical-align:middle";
}

const getURLParams = () =>{
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const next = urlParams.get('next');
    const para = document.createElement("p")
    if(next.includes('/Wiki/entries/') || next.includes('/Wiki/documents/')){
        para.innerText = "You are trying to access restricted content, please login with an authorized account:";
    }
    else if(next.includes('/Wiki/upload/')){
        para.innerText = "Login with an account that has entry creation permissions:"
    }
    document.getElementById("editable").appendChild(para);
}

const showMenu = async () => {
    if(document.getElementById("show_menu") == null) return;
    let unfocus = document.getElementById("wrapper");
    let btn_show_menu = document.getElementById("show_menu");
    let menu_bar = document.getElementById("menu_bar");

    let removed = false;

    unfocus.addEventListener("click", async () =>{
        if(removed == false){
            menu_bar.style.animation="move_menu2 150ms linear 1";
            await delay(150);
            menu_bar.classList.add("hidden");
        }
        else{
            menu_bar.style.animation="move_menu 150ms linear 1";
            removed = false;
        }
    })
    
    btn_show_menu.addEventListener("click", async () =>{
        if(menu_bar.classList.contains("hidden")){
            menu_bar.classList.remove("hidden");
            menu_bar.style.animation="move_menu 150ms linear 1";
            removed = true;
        }
        else{
            menu_bar.style.animation="move_menu2 150ms linear 1";
            await delay(150);
            menu_bar.classList.add("hidden");
        }
    })
}

function homeButton(){
    if(document.getElementById("homebutton") == null) return;
    let home_button = document.getElementById("homebutton");
    home_button.addEventListener("click", function(){
        window.location.href = "../../";
    })
}

function submitFormsWithCtrlEnter() {
    $('#form').keydown(function(event) {
      if (event.ctrlKey && event.keyCode === 13) {
        $(this).trigger('submit');
      }
    })
  }
  