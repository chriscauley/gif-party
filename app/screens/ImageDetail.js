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
  const { variants, loading, id, src, name } = props.api
  if (loading) {
    return null
  }
  return (
    <div className="flex">
      <div className="w-1/3">
        <ImageForm />
      </div>
      <div className="w-2/3">
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
