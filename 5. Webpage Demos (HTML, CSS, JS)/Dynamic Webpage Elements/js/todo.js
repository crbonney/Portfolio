
// on page load
function initialize(){
	loadToDoList();
}

//loads a previously saved todo items and displays them
function loadToDoList(){

	// get key-value pairs in local storage, store in array
	var length = localStorage.length;
	todoList = [];
	for (var i=0; i < length; i++){
		todoList[i] = localStorage.key(i);
	}

	todoList.sort();

	//build innerHTML string and insert into webpage
	var markup = "<ul>";
	for (var keyIndex in todoList){
		markup += "<li>" + todoList[keyIndex] + "</li>";
	}

	document.getElementById("itemList").innerHTML = markup;
}

// add new item to page, and store it in local storage
function saveItem() {
	var keyName = document.getElementById("todoTag");
	var keyValue = "To do item";
	localStorage.setItem(keyName.value, keyValue);

	keyName.value = "";

	// reload list with new item added
	loadToDoList();
}

// removes local storage and resets list
function clearAllItems(){
	localStorage.clear();
	loadToDoList();
}
