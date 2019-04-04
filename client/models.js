import uR from 'unrest.io'

const { Model, Int, String, APIManager, List, ForeignKey } = uR.db

class SourceImage extends Model {
  static slug = 'server.SourceImage'
  static fields = {
    id: Int(0),
    name: String(),
    src: String(),
  }
  __str__() {
    return this.name
  }
}

class PartyImage extends Model {
  static slug = 'server.PartyImage'
  static fields = {
    id: Int(0),
    source: ForeignKey('server.SourceImage'),
    resize: Int(0, { choices: [[0,'none'], 32, 64] }),
    n_frames: Int(0, { choices: [6,8,10,12,16,20,24,30,32]}),
    negate: String("",{choices: ['','red','green','blue']}),
    /*delay: Int(0),
    files: List(""),*/
  }
  static editable_fieldnames = ['source', 'resize']
}

new APIManager(SourceImage)
new APIManager(PartyImage)
