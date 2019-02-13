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

function deleteBlog(id){
        let formData = new FormData();
        alert (id);
        formData.append('blog_id', id);
        formData.append('csrfmiddlewaretoken', document.getElementById('csrfmiddlewaretoken').value);
        fetch('/blog/delete/', { 
          method: "POST", 
          body: formData 
        })
        .then(function(response) {
                console.log( "deleted " + id);
                return (response.json());
        })
}
