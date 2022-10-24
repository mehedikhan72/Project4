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

        edit_box = document.querySelector("#textarea_edit");
        if(edit_box){
            edit_box.classList.remove("textarea_light");
            edit_box.classList.add("textarea_dark");
        }

        edit_div = document.querySelector("#edit_post");
        if(edit_div){
            edit_div.classList.remove("edit_box_light");
            edit_div.classList.add("edit_box_dark");
        }

        hr = document.querySelector("#hr");
        if(hr){
            hr.classList.remove("hr_light");
            hr.classList.add("hr_dark");
        }

        document.querySelectorAll(".btn-light").forEach(btn =>{
            btn.classList.remove("btn-light");
            btn.classList.add("btn-dark");
        })

        document.querySelectorAll(".page-link").forEach(page =>{
            page.classList.remove("pagination_light");
            page.classList.add("pagination_dark");
        })

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

        edit_box = document.querySelector("#textarea_edit");
        if(edit_box){
            edit_box.classList.remove("textarea_dark");
            edit_box.classList.add("textarea_light");
        }

        edit_div = document.querySelector("#edit_post");
        if(edit_div){
            edit_div.classList.remove("edit_box_dark");
            edit_div.classList.add("edit_box_light");
        }

        hr = document.querySelector("#hr");
        if(hr){
            hr.classList.remove("hr_dark");
            hr.classList.add("hr_light");
        }

        document.querySelectorAll(".btn-dark").forEach(btn =>{
            btn.classList.remove("btn-dark");
            btn.classList.add("btn-light");
        })

        document.querySelectorAll(".page-link").forEach(page =>{
            page.classList.remove("pagination_dark");
            page.classList.add("pagination_light");
        })

        checkbox.checked = false;
        sessionStorage.setItem("mode", "light");
    }
})

// Edit post
document.addEventListener('DOMContentLoaded', function(){

    document.addEventListener('click', event =>{
        let elem = event.target;
        
        if(elem.id === 'edit_button_id'){
            post_id = elem.dataset.post_id;
        }
        
        if(elem.id === 'edit_button_id'){

            document.querySelectorAll("#post_box").forEach(t =>{
                t.classList.remove('body');
                t.classList.add('body_while_editing');
            })
            u = document.querySelector("#create_post");
            if(u){
                u.classList.remove('body');
                u.classList.add('body_while_editing');
            }

            edit_btn(post_id);
        }

        if(elem.id === 'cancel_edit_id'){
            document.querySelectorAll("#post_box").forEach(t =>{
                t.classList.add('body');
                t.classList.remove('body_while_editing');
            })
            u = document.querySelector("#create_post");
            if(u){
                u.classList.add('body');
                u.classList.remove('body_while_editing');
            }

            cancel_btn(post_id);
        }

        if(elem.id === 'save_edit_id'){
            document.querySelectorAll("#post_box").forEach(t =>{
                t.classList.add('body');
                t.classList.remove('body_while_editing');
            })
            u = document.querySelector("#create_post");
            if(u){
                u.classList.add('body');
                u.classList.remove('body_while_editing');
            }

            save_btn(post_id);
        }
    })
})
function edit_btn(post_id){
    let editmenu_popup = document.querySelector('#edit_post');
    let menu_content = document.querySelector("#textarea_edit");

    fetch(`/post/${post_id}`)
    .then(response => response.json())
    .then(post => {
        console.log("edit button clicked");
        console.log(post_id);
        menu_content.value = post[0].fields.post;
    });

    editmenu_popup.classList.remove("edit_post");
    editmenu_popup.classList.add("edit_post_clicked");
}

function cancel_btn(post_id){
    document.querySelector("#edit_post").classList.remove("edit_post_clicked");
    document.querySelector("#edit_post").classList.add("edit_post");
    document.querySelector("#textarea_edit").value= '';
    console.log("cancel button clicked");
    console.log(post_id);
}

function save_btn(post_id){
    new_post_content = document.querySelector('#textarea_edit').value;
    fetch(`/save_edited_post/${post_id}`, {
        method: 'POST',
        credentials : 'same-origin',
        headers : {
            "Accept" : 'application/json',
            'X-Requested-With'  : 'XMLHttpRequest',
            'X-CSRFToken' : getCookie("csrftoken"),
        },
        body: JSON.stringify({'new_post_content' : new_post_content})
    })
    .then(response => response.json())
    .then(post => {
        new_content = post[0].fields.post;
        likes = post[0].fields.likes_count;

        console.log("save button clicked.");
        console.log(post_id);

        document.querySelector("#edit_post").classList.remove("edit_post_clicked");
        document.querySelector("#edit_post").classList.add("edit_post");
        document.querySelector("#textarea_edit").value = '';

        e = document.getElementById(post_id);
        e.innerHTML = `<div id="${post.id}">
                        ${new_content}
                        <br>
                        <strong>${likes} likes</strong>
                      </div>`
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add and remove likes
document.addEventListener('DOMContentLoaded', function(){
    el = document.querySelectorAll('.like_button').forEach(el =>{
        el.addEventListener('click', function(){
            post_id = el.dataset.post_id;
            console.log(post_id);
            fetch(`/like_data/${post_id}`)
            .then(response => response.text())
            .then(data =>{
                console.log(data);
                if(data === "False"){
                    add_like(post_id);
                }
                else if(data === "True"){
                    remove_like(post_id)
                }
            })
        })
    })
})

function add_like(post_id){
    fetch(`/increase_likes/${post_id}`, {
        method: 'POST',
        credentials : 'same-origin',
        headers : {
            "Accept" : 'application/json',
            'X-Requested-With'  : 'XMLHttpRequest',
            'X-CSRFToken' : getCookie("csrftoken"),
        },
    })
    .then(response => response.json())
    .then(post => {
        new_content = post[0].fields.post;
        likes = post[0].fields.likes_count;

        e = document.getElementById(post_id);
        e.innerHTML = `<div id="${post.id}">
                        ${new_content}
                        <br>
                        <strong>${likes} likes</strong>
                      </div>`

        heart_btn = document.querySelectorAll('#heart_btn').forEach(btn =>{
            btn_id = btn.dataset.post_id;
            if(btn_id === post_id){
                btn.classList.remove("fa-heart-o");
                btn.classList.add("fa-heart");
            }
        })
    })
}

function remove_like(post_id){
    fetch(`/decrease_likes/${post_id}`, {
        method: 'POST',
        credentials : 'same-origin',
        headers : {
            "Accept" : 'application/json',
            'X-Requested-With'  : 'XMLHttpRequest',
            'X-CSRFToken' : getCookie("csrftoken"),
        },
    })
    .then(response => response.json())
    .then(post => {
        new_content = post[0].fields.post;
        likes = post[0].fields.likes_count;

        e = document.getElementById(post_id);
        e.innerHTML = `<div id="${post.id}">
                        ${new_content}
                        <br>
                        <strong>${likes} likes</strong>
                      </div>`
        heart_btn = document.querySelectorAll('#heart_btn').forEach(btn =>{
            btn_id = btn.dataset.post_id;

            if(btn_id === post_id){
                btn.classList.remove("fa-hearto");
                btn.classList.add("fa-heart-o");
            }
        })
    })
}

