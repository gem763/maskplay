class Session {
  constructor(entrypoint) {
    this.page = {
      home:      { order: 0, instant: false, open: false, from: 'left' },
      writer:    { order: 0, instant: false, open: false, from: 'left', blob: undefined },
      pixeditor: { order: 0, instant: true, open: false, from: 'left', src: undefined, loader: undefined },
    };

    this.entrypoint = entrypoint;
    this.home = 'home';
    this.page[this.home].open = true;
    this.store = new Store();
    this.scroll_direction = 'up';
    this.mode = { on: this.home, order: 0, prev: undefined, dasher_control: this.dasher_control };
  }


  reload_everyday() {
    const now = new Date();
    const night = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() + 1, // the next day, ...
        0, 0, 0 // ...at 00:00:00 hours
    );

    var msTillMidnight = night.getTime() - now.getTime();
    setTimeout(() => {
      location.reload();

    }, msTillMidnight);
  }


  logout() {
    fetch('/logout/')
      .then(x => {
        if (x.ok) {
          location.reload();
          console.log('successfully logged out');
        }
      });
  }

  close_page() {
    this.page[this.mode.on].open = false;
    // this.page[this.mode.on].order = 0;
    this.checkout();

    if (this.mode.on in this.page) {
      this.page[this.mode.on].open = true;
      this.page[this.mode.on].order = this.mode.order;
    }
  }

  close_pages_all() {
    while (!this.on(this.home)) {
      this.close_page();
    }
  }

  open_page(pagename, covering) {
    // if (this.on(pagename)) {
    //   setTimeout(() => {
    //     this.mode.dasher_control.open = false;
    //     this.mode.dasher_control.section = undefined;
    //   }, 200);
    //   return
    // }

    if (pagename == this.home) {
      this.close_pages_all();
      return
    }

    if (this.on('home')) {
      covering = true;
    }

    if (!covering && this.mode.on in this.page) {
      this.page[this.mode.on].open = false;

      if (this.page[this.mode.on].instant) {
        this.checkout();
      }
    }

    this.checkin(pagename);
    this.page[pagename].open = true;
    this.page[pagename].order = this.mode.order;
  }

  checkin(on) {
    console.log(`check-in to ${on}`);
    this.mode.prev = {...this.mode};
    this.mode.on = on;
    this.mode.order = this.mode.prev.order + 1;
  }

  checkout() {
    try {
      console.log(`check-out from ${this.mode.on}, back to ${this.mode.prev.on}`)
      this.mode = this.mode.prev;

    } catch(e) {
      console.log('abnormal access')
    }
  }

  on(...pages) {
    return !!pages.filter(p => this.mode.on == p).length
  }

  open_home() {
    this.open_page(this.home);
  }

  open_writer(blob) {
    this.page.writer.blob = blob;
    this.open_page('writer');
  }

  open_pixeditor(src, loader) {
    this.page.pixeditor.src = src;
    this.page.pixeditor.loader = loader;
    this.open_page('pixeditor');
  }

  open_about() {
    this.open_page('about');
  }

  contact() {
    document.location.href = 'mailto:contact@moiber.com';
  }

  fix_window_width() {
    setTimeout(() => {
      const w = document.querySelector('#moiber > .window').clientWidth;
      document.documentElement.style.setProperty('--width', w + 'px');
    }, 400);
  }

  release_window_width() {
    setTimeout(() => {
      document.documentElement.style.setProperty('--width', 'min(var(--width-max), 100vw, calc(100vh * 11 / 16))');
    }, 300);
  }
}




class Loader {
  constructor(session, baseobj) {
    this.session = session;
    this.onloading = false;
    this.loaded = false;
    this.id = undefined;
    this.url = undefined;
    Object.assign(this, baseobj);
  }

  assign(obj) {
    Object.assign(this, obj);
  }

  load() {
    if (this.loaded || this.onloading) {
      return this
    }

    this.onloading = true;

    fetch(this.url)
      .then(x => x.json())
      .then(js => {
        this.onloading = false;
        this.loaded = true;

        if (js.success) {
          this.assign(js.content);
        }
      });

    return this
  }

  // 객체만 생성 (로드는 안하기)
  static init(session, baseobj) {
    return new this(session, baseobj)
  }

  // 완전히 로드하기
  static build(session, baseobj) {
    return this.init(session, baseobj).load()
  }
}



class Pix extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/pix/${baseobj.id}`;
    this.desc = undefined;
    this.src = undefined;
    this.owner = undefined;
    this.outlink = undefined;
    this.type = undefined;
    this.tags = undefined;
  }

  assign(obj) {
    this.desc = obj.desc;
    this.src = obj.src;
    this.outlink = obj.outlink;
    this.type = obj.type;
    this.tags = obj.tags;
    this.owner = Baseboo.init(this.session, obj.owner);
  }

  static init(session, baseobj) {
    if (baseobj.id in session.store.pixstore) {
      return session.store.pixstore[baseobj.id]

    } else {
      const pix = super.init(session, baseobj);
      Vue.set(session.store.pixstore, pix.id, pix);
      return pix
    }
  }
}


class Baseboo extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/boo/${baseobj.id}/baseboo`;
    this.text = undefined;
    this.profile = undefined;
    this.collections = undefined;
    // this.collections = new Collections(session, baseobj.id);
  }

  assign(obj) {
    Object.assign(this, obj);
    this.collections = new Collections(this.session, this.id);
  }

  static init(session, baseobj) {
    if (baseobj.id in session.store.boostore) {
      return session.store.boostore[baseobj.id]

    } else {
      const boo = super.init(session, baseobj);
      Vue.set(session.store.boostore, boo.id, boo);
      return boo
    }
  }
}


class Boo extends Baseboo {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.genderlabels = undefined;
    this.stylelabels = undefined;
    this.itemlabels = undefined;
    this.styleprofile = {};
    this.wallet = undefined;
    this.researched = [];
    // this.supports = undefined;
    this.raffles = undefined;
  }

  static init(session, baseobj) {
    const boo = super.init(session, baseobj);
    // Vue.set(session.store.boostore, boo.id, boo);
    return boo
  }

  assign(obj) {
    Object.assign(this, obj);
    this.collections = new Collections(this.session, this.id);
    // this.supports = new MySupports(this.session);
    this.raffles = new MyRaffles(this.session);
    this.wallet = new Wallet(obj.wallet, this.session);
    this.signup_check();
    // this.help();
  }

  signup_check() {
    const signupinfo = sessionStorage.getItem('signupinfo');
    if (signupinfo && (this.wallet.baseinfo_inputed==false)) {
      fetch(`/signup/setbase?data=${signupinfo}`)
        .then(res => res.json())
        .then(js => { console.log(js); });

      Object.assign(this.session.user.auth, JSON.parse(signupinfo));
      sessionStorage.removeItem('signupinfo');

      // this.wallet.receive('baseinfo_input', this.wallet.amount_baseinfo_input);
      this.wallet.baseinfo_inputed = true;
      // alert(`기본정보 입력으로 ${this.wallet.amount_baseinfo_input}P가 지급되었습니다`);
      this.session.help();
    }
  }
}


class Tag extends Loader {
  constructor(session, baseobj) {
    super(session, baseobj);
    this.url = `/tag/${baseobj.id}`;
    this.pix = undefined;
    this.type = undefined;
    this.category = undefined;
    this.item = undefined;
    this.x = undefined;
    this.y = undefined;
  }

  assign(obj) {
    Object.assign(this, obj);
    this.pix = Pix.build(this.session, obj.pix);
  }
}


class Multiloader {
  constructor(session) {
    this.session = session;
    this.ids_url = undefined;
    this.ids = [];
    this.list = [];
    this.onloading = false;
    this.contentype;
    this.list_onloading = [];
  }

  load(n) {
    if (this.ids.length == 0) { return }
    if (n == 0) { return }
    if (!n) { var n = 1; }
    n = Math.min(n, this.ids.length);

    this.list_onloading = [];
    let _id;

    for (let i = 0; i < n; i++) {
      _id = this.ids.shift();
      // const content = this.contentype.build(this.session, { id:_id })

      if (_.findIndex(this.list, ['id', _id]) == -1) {
        const content = this.contentype.build(this.session, { id:_id });
        this.list.push(content);
        this.list_onloading.push(content);
      }
    };

    return this
  }

  load_ids(first) {
    this.onloading = true;
    fetch(this.ids_url)
      .then(x => x.json())
      .then(js => {
        this.onloading = false;

        if (js.success) {
          this.ids = js.ids;

          if (first) {
            var idx = this.ids.indexOf(first);
            if (idx !== -1) {
              this.ids.splice(idx, 1);
              this.ids.unshift(first);
            }
          }

          this.load(this.nloads_init);
        }
      });
  }
}


class Stylelabels extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Stylelabel;
    this.nloads_init = 20;
    this.ids_url = `/label/istylelabels`;
    this.load_ids();
  }
}

class Itemlabels extends Multiloader {
  constructor(session) {
    super(session);
    this.contentype = Itemlabel;
    this.nloads_init = 20;
    this.ids_url = `/label/iitemlabels`;
    this.load_ids();
  }
}


class Store {
  constructor() {
    // this.pixstore = {};
  }
}


class User {
  constructor(session) {
    this.auth = undefined;
    this.guest = undefined;
    this.onloading = true;
    this.loginplz = false;
    this.session = session;
    this.load();
  }

  load() {
    fetch('/user2')
      .then(x => x.json())
      .then(js => {
        if (js.mode == 0) {
          this.auth = new Auth(js.user, this.session);

        } else if (js.mode == 1) {
          this.guest = { boo: JSON.parse(js.guestboo) };

        } else {

        }

        this.onloading = false;
      });
  }

  get has_auth() {
    return this.auth ? true : false
  }

  get is_guest() {
    return this.guest ? true : false
  }

  get boo() {
    if (this.has_auth) {
      return this.auth.boo

    } else if (this.is_guest){
      return this.guest.boo
    }
  }

  get auth_ready() {
    if (this.has_auth) {
      return this.boo.loaded
    }
  }

  is_myboo(boo) {
    if (this.has_auth) {
      return this.auth.is_myboo(boo)
    }
  }

  is_following(boo) {
    return this.has_auth && !this.is_myboo(boo) && this.auth.is_following(boo.id)
  }

  follow(boo) {
    if (this.has_auth) {
      this.auth.follow(boo.id)
    }
  }

  unfollow(boo) {
    if (this.has_auth) {
      this.auth.unfollow(boo.id)
    }
  }

  get boos_fully_loaded() {
    if (this.has_auth) {
      return this.auth.boos_fully_loaded

    } else {
      return true
    }
  }
}


class Auth {
  constructor(cuser, session) {
    this.cuser = cuser;
    this.id = Number(cuser.id);
    this.name = cuser.name;
    this.gender = cuser.gender==0 ? '남성' : '여성';
    this.birth = cuser.birth;
    this.address = cuser.address;
    this.mobile = cuser.mobile;
    this.mobile_verified = cuser.mobile_verified;
    this.session = session;
    this.email = cuser.email;
    this.is_superuser = cuser.is_superuser;
    this.help = cuser.help;
    this.referal_code = cuser.referal_code;
    this.boo_selected = Number(cuser.boo_selected);
    this.boos = cuser.boo ? {[cuser.boo_selected]: Boo.build(session, cuser.boo)} : {};
    this.boos_fully_loaded = false;
  }

  reload_boos() {
    this.boos = {};
    setTimeout(() => {
      this.boos = this.cuser.boo ? {[this.cuser.boo_selected]: Boo.build(this.session, this.cuser.boo)} : {};
    }, 10);
  }

  api_get(url) {
    fetch(url)
      .then(x => x.json())
      .then(js => {
        console.log(js)
      });
  }
}
