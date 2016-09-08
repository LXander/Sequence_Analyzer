import json
import var_gen

template = '''
{
  "resourceType": "Sequence",
  "id": "f002",
  "type": "DNA",
  "coordinateSystem": 0,
  "patient": {
    "reference": "Patient/example"
  },
  "referenceSeq": {
    "referenceSeqId": {
      "coding": [
        {
          "system": "http://www.ncbi.nlm.nih.gov/nuccore",
          "code": "NC_000001.11"
        }
      ]
    },
    "strand": 1,
    "windowStart": 10453,
    "windowEnd": 101770080
  },
  "repository": [
    {
      "url": "https://www.googleapis.com/genomics/v1beta2",
      "name": "ga4gh",
      "variantId": "A1A2"
    }
  ]
}
'''

class builder:
    def __init__(self):
        self.temp = template
        self.var_gen = var_gen.var_gen()

    def build_example(self):
        example = json.loads(self.temp)
        example['variant'] = self.var_gen.vars_gen()
        return json.dumps(example)

if __name__ == "__main__":
    temp_dict = json.loads(template)
    var_generator = var_gen.var_gen()
    temp_dict['variant'] = var_generator.vars_gen()
    print (json.dumps(temp_dict,indent=4))