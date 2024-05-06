import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { HttpClientModule } from '@angular/common/http';


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MatButtonModule,
    FormsModule,
    MatInputModule,
    HttpClientModule
  ],
  exports: [
    CommonModule,
    MatButtonModule,
    FormsModule,
    MatInputModule
  ]
})
export class SharedModule { }
