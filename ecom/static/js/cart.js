var n = document.getElementsByClassName('update-cart')

for(i=0; i<n.length; i++){
    n[i].addEventListener('click', function(){
        var pname = this.dataset.product
        var action = this.dataset.action
        if(user == 'AnonymousUser'){
            if(action=='add')
        {
            if(cart[pname]==undefined)
            {
                cart[pname]= {'quantity': 1}
            }
            else
            {
                cart[pname]['quantity'] += 1
            }
        }
        else if(action=='remove')
        {
            cart[pname]['quantity'] -= 1
            if(cart[pname]['quantity'] <= 0)
            {
                delete cart[pname]
            }
        }
        else if(action=='del')
        {
            delete cart[pname]
        }

        document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"
        location.reload()
        }
        
        else{
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
                location.reload()
            })
        }

        
    })

}

