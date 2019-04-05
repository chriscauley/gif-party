import uR from 'unrest.io'

const { Model, Int, String, APIManager, StorageManager, ForeignKey } = uR.db

class SourceImage extends Model {
  static slug = 'server.SourceImage'
  static fields = {
    id: Int(0),
    name: String(),
    src: String(),
  }
  static opts = {
    n_frames: undefined,
    colors: [],
  }
  __str__() {
    return this.name
  }
}

const color_choice_hack = () => {
  return window.IMAGE.colors.map(c => c.color)
}

class PartyImage extends Model {
  static slug = 'server.PartyImage'
  static fields = {
    id: Int(0),
    source: ForeignKey('server.SourceImage'),
    resize: Int(0, { choices: [[0, 'none'], 32, 64, 128] }),
    n_frames: Int(0, { choices: [6, 8, 10, 12, 16, 20, 24, 30, 32] }),
    negate: String('', { choices: [['', 'None'], 'red', 'green', 'blue'] }),
    color_method: String('hue_rotate', {
      choices: ['hue_rotate', 'replace_color'],
    }),
    replace_color: String('', { required: false, choices: color_choice_hack }),
    delay: Int(6, { choices: [2, 4, 6, 8, 10, 12, 16, 20] }),
    fuzz: Int(3, { required: false }),
    /*delay: Int(0),
    files: List(""),*/
  }
}

new APIManager(SourceImage)
new StorageManager(PartyImage)
