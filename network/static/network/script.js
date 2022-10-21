// js for dark-mode
document.addEventListener('DOMContentLoaded', function(){
    let checkbox = document.getElementById("customSwitches");

    if (sessionStorage.getItem("mode") == "dark"){
        darkmode();
    }
    else{
        nodark();
    }

    checkbox.addEventListener('change', function(){
        if(checkbox.checked){
            darkmode();
        }
        else{
            nodark();
        }
    });

    function darkmode(){
        document.body.classList.add("dark-mode");

        document.querySelectorAll('#post_box').forEach(el => {
            el.classList.remove("eachpost");
            el.classList.add("eachpost-dark-mode");
        })

        document.querySelectorAll('.link_class').forEach(el => {
            el.classList.remove("link_light");
            el.classList.add("link_dark");
        })

        nav = document.querySelector("#navbar_id");
        nav.classList.remove("navbar-light");
        nav.classList.add("navbar-dark");
        nav_bg = document.querySelector("#navbar_id");
        nav_bg.classList.remove("bg-light");
        nav_bg.classList.add("bg-dark");

        text_box = document.querySelector("#textarea_id");
        if(text_box){
            text_box.classList.remove("textarea_light");
            text_box.classList.add("textarea_dark");
        }

        hr = document.querySelector("#hr");
        if(hr){
            hr.classList.remove("hr_light");
            hr.classList.add("hr_dark");
        }

        checkbox.checked = true;
        sessionStorage.setItem("mode", "dark");
    }

    function nodark(){
        document.body.classList.remove("dark-mode");

        document.querySelectorAll('#post_box').forEach(el => {
            el.classList.remove("eachpost-dark-mode");
            el.classList.add("eachpost");
        })

        document.querySelectorAll('.link_class').forEach(el => {
            el.classList.remove("link_dark");
            el.classList.add("link_light");
        })

        nav = document.querySelector("#navbar_id");
        nav.classList.remove("navbar-dark");
        nav.classList.add("navbar-light");

        nav_bg = document.querySelector("#navbar_id");
        nav_bg.classList.remove("bg-dark");
        nav_bg.classList.add("bg-light");

        text_box = document.querySelector("#textarea_id");

        if(text_box){
            text_box.classList.remove("textarea_dark");
            text_box.classList.add("textarea_light");
        }

        hr = document.querySelector("#hr");
        if(hr){
            hr.classList.remove("hr_dark");
            hr.classList.add("hr_light");
        }

        checkbox.checked = false;
        sessionStorage.setItem("mode", "light");
    }
})

// Edit post

document.addEventListener('click', event =>{
    let elem = event.target;

    if(elem.className === 'edit_button'){
        document.querySelector("#edit_post").classList.remove("edit_post");
        document.querySelector("#edit_post").classList.add("edit_post_clicked");
    }

    if(elem.className === 'cancel_edit'){
        document.querySelector("#edit_post").classList.remove("edit_post_clicked");
        document.querySelector("#edit_post").classList.add("edit_post");
    }
})
