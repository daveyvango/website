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
        
        if (confirm("Are you sure you want to delete this post?")){
            alert ( "You deleted it" );
            document.getElementById('delete_blog').submit();
        }
        else {
            alert ( "Good idea.  You can always delete later.");
        }
/*        let formData = new FormData();
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
        */
}
