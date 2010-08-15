/**
 * @author Subramanyan Murali subram@yahoo-inc.com
 * @class remoteData
 * @Usage
 * YAHOO.remoteData.fetch(url, callBack, scopeObj, trackWithID);
 * Using the dynamic script attach method, we can only get the data across a
 * call back function specified part of hte &callback=cb parameter. But if
 * we want to have control over the call back function from the javascript space
 * then we can use this remoteData class. Using closures, the user provided
 * call back will be called for every data fetch request. The data will always
 * be fetched using a single fetch function handled by the class. The class
 * also handle transaction IDs so that the remoteData singleton can be
 * used to fetch data from multiple data sources at the same time with out
 * causing collisions in the custom call back and scope objects
 *
 * @TODO Implement caching for similar url data fetches
 * @TODO Normalize the response as responseText/responseJSON property
 *       with transaction id and other Ajax specific data for a response object
 * 
 */

   // Remote Data name space
   if(typeof(YAHOO) !="undefined" && typeof(YAHOO.namespace) != "undefined")
      YAHOO.namespace("remoteData");
   else
      YAHOO = {};
   /**
    * Singleton to handle all the cross domain request
    * @class remoteData
    * @member YAHOO
    * @final
    */
   YAHOO.remoteData = new function()
   {
     /**
      * The Callback object strore/cache. This private member will cache
      * all the callback function calls and scope objects
      * @property callBack
      * @type Object
      * @member remoteData
      */
     this.callBack = {};
     
     /**
      * id of the script node created to do the remote data fetch request
      * @property id
      * @private
      * @member remoteData
      * @type String
      */
     var id = "data_fetch_script_";
     
     /**
      * Method to return a unique 5 digit number
      * @method getUniqueNumber
      * @member remoteData
      * @private
      * @returns {number} Unique 5 digit number
      */
     var getUniqueNumber = function() {
        var _rnd = ((new Date().getTime()) / Math.pow(10, 5)).toString();
        return parseInt(_rnd.substr(_rnd.lastIndexOf(".")+1), 10);  
     };
     
     /**
      * The fetch data method used to initiate the cross side data fetch
      * request
      * @method fetch
      * @member remoteData
      * @param url {string} The data fetch url string with JSONP response
      * @param callBack {function} The user defined Callback function
      * @param scope {object} The scope of the call
      * @param track_with_id {boolean} When set to true, each data fetch
      *                                request will be tracked with a transaction
      *                                id. Default is TRUE
      * @returns {void}
      */
     this.fetch = function(url, callBack, scope, track_with_id) {
      
        var tran_id = "default";
        var scr = null;
        var u = getUniqueNumber();
        
        if(typeof(useJson) == "undefined")
          useJson = true;
        if(typeof(url) != "string" || url == "") {
          alert("Url is needed for fetching data");
          return;
        }
        if(typeof(track_with_id) == "undefined")
           track_with_id = true;
      
        if(track_with_id)
            tran_id = "tran_" + u;
            
        if(typeof(callBack)  == "function") {
          this.callBack[tran_id] = {
                      fn : callBack,
                      sc : (scope)?scope:window,
                      tid: tran_id
          };
        }
        
        if(document.getElementById(id+u) == null)
        {
           scr = document.createElement("script");
           scr.type="text/javascript";
           scr.id = id + tran_id;
        }
        else
           scr = document.getElementById(id+tran_id);
         
        url = url + "&format=json&callback=YAHOO.remoteData.handle_"+tran_id;
      
        // Cross domain request that returns the data wrapped in the callback function
        //YAHOO.remoteData.handle({'........'})
        scr.src= url;
      
        if(track_with_id) {
            YAHOO.remoteData["handle_"+tran_id] = function(o) {
               YAHOO.remoteData.handle(o, tran_id);
            };
        }
        document.body.appendChild(scr);
     }
     /**
      * The method to handle the response. This method will call the user
      * defined callback under proper scope
      * @method handle
      * @member remoteData
      * @param o {object} The response data object from the remote call
      * @param _tr {string} The transaction id of the operation
      */
     this.handle = function(o, _tr)
     {
        if(!this.callBack[_tr])
           return;
        var _c = this.callBack[_tr];
        _c.fn.call(_c.sc, o);
        var _src = document.getElementById(id+_tr);
        _src.parentNode.removeChild(_src);
        
        delete(this.callBack[_tr]);
        delete(YAHOO.remoteData["handle_"+_tr]);
     }
   };