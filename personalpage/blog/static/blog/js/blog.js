function fetchBlog(id){
        fetch('/blog/' + id + '/json')
        .then(function(response) {
                return (response.json());
        })
        .then(function(data) {
                console.log(data);
                document.getElementById('blog_body').innerHTML = data.text;
        });
}
