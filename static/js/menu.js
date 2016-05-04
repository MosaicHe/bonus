function init_menu(id) {
	var Menu = document.getElementById(id);
	var Menus = Menu.getElementsByTagName('span');
	for (var i = 0; i < Menus.length; i++) {
		Menus[i].onclick = function() {
			expand(this);
		}
	}
}

function expand(parentMenu) {
	var child = parentMenu.parentNode.getElementsByTagName('ul');
	if (child.length > 0) {
		if (child[0].className == 'menu-undis') {
			/* ��������ͬ���˵����Ӳ˵������������Ƿ���Ҫ������������ע��ȥ�������� */
			/*var childMenus = parentMenu.parentNode.parentNode.getElementsByTagName('ul');
			for (var i = 0; i < childMenus.length; i++) {
				childMenus[i].className = 'undis';
			}*/
			parentMenu.innerHTML = parentMenu.innerHTML.replace('+', '-');
			child[0].className = '';
		} else {
			parentMenu.innerHTML = parentMenu.innerHTML.replace('-', '+');
			child[0].className = 'menu-undis';
		}
	} else {
	}
}