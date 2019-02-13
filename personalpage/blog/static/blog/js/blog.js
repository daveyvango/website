function fetchBlog(id){
        fetch('/blog/' + id + '/json')
        .then(function(response) {
                return (response.json());
        })
        .then(function(data) {
                console.log(data.text);
                let blog_text = data.text
                document.getElementById('blog_body').innerHTML = blog_text;
        });
}

function fetchBlogToEdit(id){
        fetch('/blog/' + id + '/json')
        .then(function(response) {
                return (response.json());
        })
        .then(function(data) {
                console.log(data);
                document.getElementById('post_text').value = data.text;
        });
}
