import { Directive } from '@angular/core';
import { NG_VALIDATORS, Validator, AbstractControl, ValidationErrors } from '@angular/forms';

const StrongPasswordRegx: RegExp = /^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d).{8,}$/;

@Directive({
  selector: '[strongPassword]',
  providers: [{provide: NG_VALIDATORS, useExisting: StrongPasswordDirective, multi: true}]
})
export class StrongPasswordDirective implements Validator {
  validate(control: AbstractControl): ValidationErrors | null {
    const value: string = control.value;
    if (!value || !value.match(StrongPasswordRegx)) {
      return { 'strongPassword': true };
    }
    return null;
  }
}