import React from 'react';
import { useIsFocused } from '@react-navigation/native';

// React Navigation 7 removed the `unmountOnBlur` screen option. These screens relied on it to
// refetch their data every time they are opened, so render them only while they are focused.
// Wrap at module level (not inside render) so the wrapped component keeps a stable identity.
export default function unmountOnBlur(Component) {
  function UnmountOnBlur(props) {
    return useIsFocused() ? <Component {...props} /> : null;
  }
  UnmountOnBlur.displayName = `UnmountOnBlur(${Component.displayName || Component.name || 'Screen'})`;
  return UnmountOnBlur;
}
