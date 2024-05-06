import { Component } from '@angular/core';
import { MenuService } from '../services/menu.service';
import { HttpClient } from '@angular/common/http';

interface MenuItem {
  id: number;
  name: string;
}


@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent {

  menuData!: { [type: string]: MenuItem[] };
  selectedItems: MenuItem[]= [];
  menuCategories!: string[];
  cantidadComidas: string = "1";
  requestDone:boolean = false;
  message:string = "";

  constructor(private menuService:MenuService, private http: HttpClient) { }

  ngOnInit(): void {
    

    this.menuService.getMenus().subscribe((data:any)=>{
      var responseSatus = data.status;
      if(responseSatus == 200){
        this.menuData = data.data;
        console.log(this.menuData);
      }
    })
  }

  getKeys(menuData: { [type: string]: MenuItem[] }) {
    return Object.keys(menuData);
  }

  toggleSelection(item: MenuItem) {
    const existe = this.selectedItems.find(selectedItem => selectedItem.id === item.id);

    if(existe){
      this.selectedItems = this.selectedItems.filter(selectedItem => selectedItem.id !== item.id);
    }else{
      this.selectedItems.push(item);
    }
  }

  enviarSeleccion() {
    console.log(this.cantidadComidas)
    if (this.cantidadComidas === "1") {
      if (Object.keys(this.selectedItems).length > 1) {
        // Deseleccionar todos los elementos checkbox
        const checkboxes = Array.from(document.querySelectorAll<HTMLInputElement>('input[type="checkbox"]'));
        checkboxes.forEach((checkbox: HTMLInputElement) => {
          checkbox.checked = false;
        });
  
        // Vaciar la lista selectedItems
        this.selectedItems = [];

        alert("No puedes enviar mas de 1 seleccion de comida.")
      } else if(Object.keys(this.selectedItems).length < 2){
        alert("Debes seleccionar 1 comida.")
      }else {
        // Enviar selección
        var request = "";

        var item = this.selectedItems[0];
        request += "MealName1="+item.id;
        

        console.log(request)
        this.hacerConsulta(request);
        console.log()
      }
    } else if (this.cantidadComidas === "2") {
      console.log("esteetet")
      if (Object.keys(this.selectedItems).length > 2) {
        // Deseleccionar todos los elementos checkbox
        const checkboxes = Array.from(document.querySelectorAll<HTMLInputElement>('input[type="checkbox"]'));
        checkboxes.forEach((checkbox: HTMLInputElement) => {
          checkbox.checked = false;
        });
  
        // Vaciar la lista selectedItems
        this.selectedItems = [];

        alert("No puedes enviar mas de 2 seleccion2s de comida.")
      } else if(Object.keys(this.selectedItems).length < 2){
        alert("Debes seleccionar 2 comidas.")
      }else {
        // Enviar selección
        var request = "";
        
        var item = this.selectedItems[0];
        request += "MealName1="+item.id;

        var item2 = this.selectedItems[1];
        request += "&MealName2="+item2.id;

        console.log(request)
        this.hacerConsulta(request);
      }
    }
  
    
  }

  hacerConsulta(entry:string){
    console.log("haciendo consulta");

    
  }
}
