import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MenuService {

  constructor(private http:HttpClient) { }

  getMenus():Observable<any>{
    return this.http.get<any>('https://us-central1-groovy-rope-416616.cloudfunctions.net/obtener-menu');
  }

  getRecomendacion(entry:string):Observable<any>{
    const url = 'https://us-west1-groovy-rope-416616.cloudfunctions.net/';
    var totalurl = url + "meal_recommendation?" + entry;
    return this.http.get<any>(totalurl);
  }
}
