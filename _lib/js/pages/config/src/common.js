/**
 * Get the DOM of an element
 */
function ctd(target){
    // If this is an Element, return the DOM
    if (target && target.nodeName)  return target;                  // If this is an Element, return the DOM

    // If this is a string reference
    if (typeof target === 'string' || target instanceof String) {
        let dom = document.getElementById(target);                  // See if the string is an element's HTML ID
        if (dom) {                                                  // If the string is an element's HTML ID; return the DOM
            return dom;
        }
    }

    else{                                                           // If attempting to fetch the target
        throw new Error('DOM not found');     // Throw an error
    }
}

export default {
    getDom: function (target){
        return ctd(target);
    },
    loading: {
        hide: function(){
            let elem = document.querySelectorAll('#loading_effect');        // Find all the matching elements
            for (let i = 0; i < elem.length; i++) {                         // Loop through each element
                elem[i].parentNode.removeChild(elem[i]);                    // Add the 'hide' class
            }
        },
        show: function(){
            let dom = ctd('c_main');

            // Create the loading graphic
            let loadingDom = document.createElement('div');
            loadingDom.setAttribute('class', 'loading');
            loadingDom.id = 'loading_effect';
            loadingDom.innerHTML = "<div class='spinner'><div class='bounce1'></div><div class='bounce2'></div><div class='bounce3'></div></div>";

            // Move inside to bottom
            dom.appendChild(loadingDom);
        }
    }
}