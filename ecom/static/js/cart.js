var n = document.getElementsByClassName('update-cart')

for(i=0; i<n.length; i++){
    n[i].addEventListener('click', function(){
        var pname = this.dataset.product
        var action = this.dataset.action
        console.log('product name:', pname,'action:',action)
        console.log('product Name:', pname,'action:',action)

        console.log('USER:', user)
        if(user == 'AnonymousUser'){
            console.log('no you')
        }
        else{
            updateUserOrder(pname,action)
        }

        
    })

}


function updateUserOrder(pname,action){
    console.log('yess yess hmm yess')

    var url = '/update_item/'
    fetch(url,{
        method : 'POST',
        headers:{ 'Content-Type': 'application/json',
                  'X-CSRFToken' : csrftoken,
    },
        body:JSON.stringify({'pname': pname,'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:',data)
    })
}