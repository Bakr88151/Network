document.addEventListener('DOMContentLoaded', () => {
    load_posts(1);
    configure_follow_button();
    document.querySelector('#follow_button').addEventListener('click', () => follow_or_unfollow())
})

var page_num = 1;

function configure_follow_button(){
    const button = document.querySelector('#follow_button');
    const is_following = document.querySelector('#is_following').value;
    if (is_following == 'True'){
        button.innerHTML = "Unfollow";
        button.className = 'btn btn-danger';
    }else{
        button.innerHTML = 'Follow';
        button.className = 'btn btn-primary';
    }
}

function follow_or_unfollow(){
    var is_following = document.querySelector('#is_following');
    if (is_following.value == 'True'){
        fetch(`/profile/${document.querySelector('#profile_id').value}`, {
            method: 'POST',
            body: JSON.stringify({
                follow: false,
                profile_id: document.querySelector('#profile_id').value
            })
          })
          .then(response => response.text())
          .then(value => {console.log(value)})
        is_following.value = 'False';
        configure_follow_button();
    }else{
        fetch(`/profile/${document.querySelector('#profile_id').value}`, {
            method: 'POST',
            body: JSON.stringify({
                follow: true,
                profile_id: document.querySelector('#profile_id').value
            })
          })
          .then(response => response.text())
          .then(value => {console.log(value)})
        is_following.value = 'True';
        configure_follow_button();
    }
}
function nex_pre_buttons(){
    const pag_len = document.querySelector('#pag_len').value;
    if (page_num == 1){
        document.querySelector('#previous').className = 'page-item disabled';
    }else{
        document.querySelector('#previous').className = 'page-item';
    }
    if (page_num == pag_len){
        document.querySelector('#next').className = 'page-item disabled';
    }else{
        document.querySelector('#next').className = 'page-item';
    }
}

function next(){
    load_posts(parseInt(page_num) + 1);
}


function previous(){
    load_posts(parseInt(page_num) - 1);
}


function edit_post(post_id, container, innitial_value){
    container.innerHTML = '';
    const text_area = document.createElement('textarea');
    text_area.className = 'content-input';
    const submit = document.createElement('button')
    submit.innerHTML = 'Post';
    submit.className = 'btn btn-primary';
    text_area.value = innitial_value;
    container.append(text_area);
    container.append(submit);
    text_area.focus();
    submit.addEventListener('click', function(){
        console.log('clicked')
        if(text_area.value != ''){
            fetch('/submitpost', {
                method: 'PUT',
                body: JSON.stringify({
                    id: post_id,
                    content: text_area.value,
              })
              }).then(() => load_posts(page_num))
        }
        load_posts(page_num)
    })   
}


function like_or_unlike(img, id){
    if(img.src=='https://i.ibb.co/LJTJ3H1/Pngtree-vector-heart-icon-4187108.png'){
        like_post(id);
        likes = img.parentElement;
        likes.innerHTML = parseInt(likes.innerHTML) + 1;
        img.src = 'https://i.ibb.co/WHx8PCw/Pngtree-vector-heart-icon-4187108red.png';
        likes.append(img);
    }else{
        unlike_post(id);
        likes = img.parentElement;
        likes.innerHTML = parseInt(likes.innerHTML) - 1;
        img.src = 'https://i.ibb.co/LJTJ3H1/Pngtree-vector-heart-icon-4187108.png';
        likes.append(img);
    }
}


function like_post(post_id){
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            task: 'like',
            post_id: post_id,
        })
    })
}


function unlike_post(post_id){
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            task: 'unlike',
            post_id: post_id,
        })
    })
}


function load_posts(page){
    fetch(`/profileposts/${page}`,{method : 'POST', body: JSON.stringify({
        id: document.querySelector('#profile_id').value,
  })})
    .then(response => response.json())
    .then(result => {
        document.querySelector('#posts').innerHTML = '';
        result.forEach(item =>{
            const container = document.createElement('div');
            container.className = 'my_container';
            const poster_link = document.createElement('a')
            poster_link.href = `/profile/${item.poster_id}`;
            const poster = document.createElement('h4');
            poster.innerHTML = item.poster;
            poster_link.append(poster)
            const post_contente = document.createElement('div');
            post_contente.className = 'content';
            post_contente.innerHTML = item.content;
            const timestamp = document.createElement('div');
            timestamp.innerHTML = item.timestamp;
            const likes = document.createElement('div');
            likes.className = 'likes';
            likes.innerHTML = item.likes;
            const like_img = document.createElement('img');
            var liked = item.liked
            if(!item.liked){
                like_img.src = 'https://i.ibb.co/LJTJ3H1/Pngtree-vector-heart-icon-4187108.png';
            }else{
                like_img.src = 'https://i.ibb.co/WHx8PCw/Pngtree-vector-heart-icon-4187108red.png';
            }
            like_img.addEventListener('click', () => {
                like_or_unlike(like_img, item.id)
            })
            likes.append(like_img);
            const edit = document.createElement('button');
            edit.innerHTML = 'Edit';
            edit.className = 'edit_button';
            container.append(poster_link);
            container.append(post_contente);
            container.append(timestamp);
            container.append(likes);
            if(item.poster_id == document.querySelector('#poster').value){
                container.append(edit);
                edit.onclick = () => {
                    edit_post(item.id, edit.parentElement, item.content)
                }    
            }
            document.querySelector('#posts').append(container);
        })
    })
    page_num = page;
    nex_pre_buttons();
}