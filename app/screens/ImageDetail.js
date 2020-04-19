import React from 'react'
import RestHook from '@unrest/react-api'
import Form from '@unrest/react-jsonschema-form'

const withImage = RestHook('/api/server/SourceImage/${match.params.object_id}/')
const withImageSchema = RestHook('/api/schema/PartyImage/')

const ImageForm = withImageSchema(props => {
  const { loading, schema } = props.api
  const initial = {}
  if (loading) {
    return null
  }
  schema.properties.replace_color.enum = []
  schema.properties.replace_color.enumNames = []
  props.colors.forEach(({color, count}) => {
    schema.properties.replace_color.enum.push(color)
    color = color.replace('srgba', 'rgba')
    schema.properties.replace_color.enumNames.push(
      <span className="w-4 h-4" style={{background: color}}></span>
    )
  })
  Object.entries(schema.properties).forEach( ([key, field]) => {
    if (field.hasOwnProperty('default')) {
      initial[key] = field.default
      if (initial[key] === null) {
        initial[key] = ''
      }
      delete field.default
    }
  })
  return <Form schema={props.api.schema} initial={initial} />
})

export default withImage(props => {
  const { variants, loading, id, src, name, colors } = props.api
  if (loading) {
    return null
  }
  return (
    <div className="flex">
      <div className="w-1/3 p-4">
        <ImageForm colors={colors} />
      </div>
      <div className="w-2/3 p-4">
        {variants.map(({src, name}) => (
          <div key={name}>
            <img src={src} />
            {name}
          </div>
        ))}
      </div>
    </div>
  )
})
