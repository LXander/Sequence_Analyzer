from flask_wtf import Form
from wtforms import SelectField,StringField,SubmitField,validators,SelectMultipleField

methods_choice = {'VCF Comparison':'VCF Comparison','Vcfeval + Hap.py Comparison':'Vcfeval + Hap.py Comparison'}
standard_sequence_choice = {'NA12878-NISTv2.19':'NA12878-NISTv2.19','NA12878-GIABv3.2':'NA12878-GIABv3.2','HG002-GIABv3.2':'HG002-GIABv3.2'}

class CompareFoem(Form):
    methods = SelectField('Methods',coerce=str , choices=[('VCF Comparison','VCF Comparison'),('Vcfeval + Hap.py Comparison','Vcfeval + Hap.py Comparison')])
    standardsequence = SelectField('Standard String',coerce=str,choices=[('NA12878-NISTv2.19','NA12878-NISTv2.19'),('NA12878-GIABv3.2','NA12878-GIABv3.2'),('HG002-GIABv3.2','HG002-GIABv3.2')])
    MultipleSequence = SelectMultipleField('Multiple String',coerce=str,choices=[('NA12878-NISTv2.19','NA12878-NISTv2.19'),('NA12878-GIABv3.2','NA12878-GIABv3.2'),('HG002-GIABv3.2','HG002-GIABv3.2')])

    submit = SubmitField("Compare")


class SearchForm(Form):
    GeneName = StringField('Name',[validators.required()])
    submit = SubmitField("Search")